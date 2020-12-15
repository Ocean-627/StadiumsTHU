from itertools import chain
from operator import attrgetter
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from django.http import JsonResponse
from app.utils.utils import *
from app.utils.manager_serializer import *
from app.utils.filter import *
from app.utils.pagination import *
from app.utils.authtication import ManagerAuthtication
# from apscheduler.scheduler import Scheduler
import time
import datetime
import pytz

'''
定时事件
'''


def daily_task():
    print("Start daily update...")
    # 删除旧数据
    now_date = calculateDate(datetime.datetime.now().strftime('%Y-%m-%d'), 1)
    old_date = datetime.datetime.now().strftime('%Y-%m-%d')
    durations = Duration.objects.all()
    delete_durations = durations.filter(date=old_date)
    delete_durations.delete()

    # 修改场地预订时间修改信息使之生效
    changeDurations = ChangeDuration.objects.all()
    for changeDuration in changeDurations:
        changeDate = calculateDate(now_date, changeDuration.courtType.stadium.foreDays - 1)
        courtType = changeDuration.courtType
        if not judgeDate(changeDuration.date, changeDate):
            courtType.openingHours = changeDuration.openingHours
            courtType.duration = changeDuration.duration
            courtType.price = changeDuration.price
            courtType.membership = changeDuration.membership
            courtType.openState = changeDuration.openState
        elif not judgeDate(changeDuration.date, now_date):
            courtType.openingHours = changeDuration.openingHours
            courtType.duration = changeDuration.duration
            courtType.price = changeDuration.price
            courtType.membership = changeDuration.membership
            courtType.openState = changeDuration.openState
            courtType.save()

            # 更新场馆信息
            openHours = courtType.split(" ")
            for openHour in openHours:
                startTime, endTime = openHour.split('-')
                if judgeTime(courtType.stadium.openTime, startTime) > 0:
                    courtType.stadium.startTime = startTime
                if judgeTime(courtType.stadium.endTime, endTime) < 0:
                    courtType.stadium.endTime = endTime
                courtType.stadium.save()

    # 添加新数据
    courtTypes = CourtType.objects.all()
    for courtType in courtTypes:
        changeDate = calculateDate(now_date, courtType.stadium.foreDays - 1)
        openHours = courtType.openingHours.split(" ")
        for court in courtType.court_set.all():
            for openHour in openHours:
                startTime, endTime = openHour.split('-')
                totalSeconds = judgeTime(endTime, startTime)
                seconds = judgeTime(courtType.duration, "00:00")
                for k in range(int(totalSeconds // seconds)):
                    endTime = (datetime.datetime.strptime(str(startTime), "%H:%M") + datetime.timedelta(
                        seconds=seconds)).strftime('%H:%M')
                    myDuration = Duration(stadium=courtType.stadium, court=court, startTime=startTime, endTime=endTime,
                                          date=changeDate, openState=courtType.openState, accessible=1,
                                          courtType=courtType)
                    myDuration.save()
                    startTime = endTime

    # 将用户移出黑名单
    changeDate = calculateDate(now_date, -100)
    User.objects.all().filter(blacklist=changeDate).update(blacklist="", defaults=0)

    # 添加场地占用事件
    addEvents = AddEvent.objects.all().filter(date=now_date)
    for addEvent in addEvents:
        myDurations = addEvent.court.duration_set.all().filter(date=now_date)
        for myDuration in myDurations:
            if judgeAddEvent(addEvent.startTime, addEvent.endTime, myDurations.startTime, myDurations.endTime):
                myDuration.openState = 0
                myDuration.save()

    # 将在有效期之外的违约记录设置为失效
    Default.objects.all.filter(date=changeDate).update(valid=False)
    print("Finished!")


def minute_task():
    # 判断违约并记录违约事件
    print("Start minute update...")
    tz = pytz.timezone('Asia/Shanghai')
    myDate = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
    myTime = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%H:%M')
    reserveEvents = ReserveEvent.objects.filter(date=myDate)
    for reserveEvent in reserveEvents:
        if judgeTime(reserveEvent.startTime,
                     calculateTime(myTime, 600)) < 0 and reserveEvent.checked == 0 and reserveEvent.cancel == 0:
            print("default!")
            reserveEvent.checked = 1
            reserveEvent.user.defaults += 1
            reserveEvent.save()
            default = Default(user=reserveEvent.user, date=myDate, time=myTime)
            default.save()
            if reserveEvent.user.defaults == 3:
                reserveEvent.user.blacklist = myDate
            reserveEvent.user.save()
    print("Finished!")


'''
若代码已经部署到服务器上，在本机上运行后端时务必将以下四行注释掉，否则会更改服务器数据库
'''

# sched = Scheduler()
# sched.add_cron_job(daily_task, hour=16, minute=0)
# sched.add_interval_job(minute_task, seconds=60)
# sched.start()


class LogonView(CreateAPIView):
    """
    管理员注册
    TODO: 目前是直接注册，日后应该加入验证环节
    """
    serializer_class = LogonSerializer


class LoginView(APIView):
    """
    管理员登录
    """

    def post(self, request):
        req_data = request.data
        userId = req_data.get('userId')
        password = req_data.get('password')
        obj = Manager.objects.filter(userId=userId, password=password).first()
        if not obj:
            return Response({'error': 'Login failed'})
        loginToken = md5(userId)
        obj.loginToken = loginToken
        obj.save()
        url = None
        if obj.image:
            url = obj.image.url
        return Response(
            {'message': 'ok', 'id': obj.id, 'username': obj.username, 'image': url, 'loginToken': loginToken})


class LogoutView(APIView):
    """
    管理员注销
    """
    authentication_classes = [ManagerAuthtication]

    def post(self, request):
        manager = request.user
        manager.loginToken = ''
        manager.save()
        ret = JsonResponse({'message': 'ok'})
        ret.delete_cookie('loginToken')
        return ret


class ManagerView(APIView):
    """
    管理员信息
    """
    authentication_classes = [ManagerAuthtication]

    def get(self, request):
        manager = request.user
        manager = ManagerSerializer(manager, many=False)
        return Response(manager.data)

    def post(self, request):
        req_data = request.data
        ser = ManagerSerializer(data=req_data)
        if not ser.is_valid():
            return Response({'error': ser.errors})
        ser.update(request.user, ser.validated_data)
        return Response({'message': 'ok'})


class StadiumView(ListAPIView):
    """
    场馆信息
    """
    # authentication_classes = [ManagerAuthtication]
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializerForManager
    filter_class = StadiumFilter

    def post(self, request):
        req_data = request.data
        ser = StadiumSerializerForManager(data=req_data)
        if not ser.is_valid():
            return Response({'error': ser.errors})
        stadium = Stadium.objects.filter(id=ser.validated_data.get('stadium_id')).first()
        ser.update(stadium, ser.validated_data)
        return Response({'message': 'ok'})


class CourtView(ListAPIView):
    """
    场地信息
    """

    # authentication_classes = [ManagerAuthtication]
    queryset = Court.objects.all()
    serializer_class = CourtSerializer
    filter_class = CourtFilter


class CourtTypeView(ListAPIView):
    """
    场地类型信息
    """
    queryset = CourtType.objects.all()
    serializer_class = CourtTypeSerializer
    filter_class = CourtTypeFilter


class DurationView(ListAPIView):
    """
    时段信息
    """
    # authentication_classes = [ManagerAuthtication]
    queryset = Duration.objects.all()
    serializer_class = DurationSerializer
    filter_class = DurationFilter


class ReserveEventView(ListAPIView):
    """
    预约信息
    """
    # authentication_classes = [ManagerAuthtication]
    queryset = ReserveEvent.objects.all()
    serializer_class = ReserveEventSerializer
    filter_class = ReserveEventFilter


class ChangeScheduleView(CreateAPIView):
    """
    修改场馆开放时间相关
    """
    authentication_classes = [ManagerAuthtication]
    serializer_class = ChangeScheduleSerializer


class ChangeDurationView(ListAPIView, CreateAPIView):
    """
    修改预约时段信息
    """

    authentication_classes = [ManagerAuthtication]
    queryset = ChangeDuration.objects.all()
    serializer_class = ChangeDurationSerializer
    filter_class = ChangeDurationFilter


class AddEventView(ListAPIView):
    """
    添加场地占用事件信息
    """
    authentication_classes = [ManagerAuthtication]
    queryset = AddEvent.objects.all()
    serializer_class = AddEventSerializer
    filter_class = AddEventFilter

    def post(self, request):
        req_data = request.data
        ser = AddEventSerializer(data=req_data)
        if not ser.is_valid():
            return Response({'error': ser.errors})
        addEvent = ser.save(manager=request.user)
        startTime = addEvent.startTime
        endTime = addEvent.endTime
        myDurations = addEvent.court.duration_set.all().filter(date=addEvent.date)
        for myDuration in myDurations:
            if judgeAddEvent(startTime, endTime, myDurations.startTime, myDurations.endTime):
                myDuration.openState = 0
                try:
                    reserveEvent = ReserveEvent.objects.get(duration_id=myDuration.id)
                    reserveEvent.cancel = 1
                    reserveEvent.save()
                except:
                    pass
                myDuration.save()
        return Response({'message': 'ok'})


class UserView(ListAPIView):
    """
    用户信息
    """
    # authentication_classes = [ManagerAuthtication]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    filter_class = UserFilter

    def put(self, request):
        req_data = request.data
        user = User.objects.filter(id=req_data.get('user_id')).first()
        if not user:
            return Response({'error': 'Invalid user_id'})
        if user.blacklist == "0":
            myDate = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime(
                '%Y-%m-%d')
            user.blacklist = myDate
        else:
            Default.objects.all().filter(user=user).update(cancel=1)
            user.defaults = 0
            user.blacklist = "0"
        user.save()
        return Response({'message': 'ok'})


class HistoryView(APIView):
    """
    历史操作信息
    """
    authentication_classes = [ManagerAuthtication]

    def get(self, request):
        manager = request.user
        changeDuration = manager.changeduration_set.all()
        addEvent = manager.addevent_set.all()
        myOperations = sorted(chain(changeDuration, addEvent), key=attrgetter('time'), reverse=True)
        operations = [model_to_dict(myOperation, fields=['time', 'type', 'id']) for myOperation in myOperations]
        return JsonResponse({'operations': operations})


class StadiumImageView(CreateAPIView):
    """
    场馆图片信息
    """
    # authentication_classes = [ManagerAuthtication]
    serializer_class = StadiumImageSerializer


class SessionView(ListAPIView, CreateAPIView):
    """
    会话信息
    """
    authentication_classes = [ManagerAuthtication]
    queryset = Session.objects.all()
    serializer_class = SessionSerializerForManager
    filter_class = SessionFilter
    pagination_class = SessionPagination

    def put(self, request):
        req_data = request.data
        ser = SessionSerializer(data=req_data)
        if not ser.is_valid():
            return Response({'error': ser.errors})
        session = Session.objects.get(id=req_data.get('session_id'))
        ser.update(session, ser.validated_data)
        return Response({'message': 'ok'})


class MessageView(ListAPIView, CreateAPIView):
    """
    消息
    """
    authentication_classes = [ManagerAuthtication]
    queryset = Message.objects.all()
    serializer_class = MessageSerializerForManager
    filter_class = MessageFilter


class DefaultView(ListAPIView, CreateAPIView):
    """
    违约记录
    """
    authentication_classes = [ManagerAuthtication]
    queryset = Default.objects.all()
    serializer_class = DefaultSerializer
    filter_class = DefaultFilter
    pagination_class = DefaultPagination

    def put(self, request):
        req_data = request.data
        default = Default.objects.filter(id=req_data.get('default_id')).first()
        if not default:
            return Response({'error': 'Invalid default_id'})
        if default.cancel == 1:
            return Response({'error': 'manager has cancelled this record.'})
        default.cancel = 1
        default.save()
        default.user.defaults -= 1
        default.user.blacklist = "0"
        default.user.save()
        return Response({'message': 'ok'})

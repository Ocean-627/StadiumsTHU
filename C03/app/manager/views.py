from itertools import chain
from operator import attrgetter
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from django.http import JsonResponse
from app.utils.utils import *
from app.utils.manager_serializer_resource import *
from app.utils.manager_serializer_event import *
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
    old_date = calculateDate(datetime.datetime.now().strftime('%Y-%m-%d'), -1)
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')
    durations = Duration.objects.all()
    delete_durations = durations.filter(date=old_date)
    delete_durations.delete()

    # 修改场地预订时间修改信息使之生效
    changeDurations = ChangeDuration.objects.all()
    for changeDuration in changeDurations:
        if changeDuration.state == 1:
            continue
        if not judgeDate(changeDuration.date, now_date):
            courtType = changeDuration.courtType
            courtType.openingHours = changeDuration.openingHours
            courtType.duration = changeDuration.duration
            courtType.price = changeDuration.price
            courtType.membership = changeDuration.membership
            courtType.openState = changeDuration.openState
            courtType.save()

            # 更新场馆信息
            openHours = courtType.openingHours.split(" ")
            for openHour in openHours:
                startTime, endTime = openHour.split('-')
                if judgeTime(courtType.stadium.openTime, startTime) > 0:
                    courtType.stadium.openTime = startTime
                if judgeTime(courtType.stadium.closeTime, endTime) < 0:
                    courtType.stadium.closeTime = endTime
                courtType.stadium.save()

    # 添加新数据
    courtTypes = CourtType.objects.all()
    for courtType in courtTypes:
        changeDate = calculateDate(now_date, courtType.stadium.foreDays - 1)
        try:
            changeDuration = ChangeDuration.objects.filter(courtType=courtType, is_active=True)[0]
            openHours = changeDuration.openingHours.split(" ")
            duration = changeDuration.duration
            changeDuration.state = 2
            changeDuration.save()
        except:
            openHours = courtType.openingHours.split(" ")
            duration = courtType.duration
        seconds = judgeTime(duration, "00:00")
        for openHour in openHours:
            for court in courtType.court_set.all():
                startTime, endTime = openHour.split('-')
                totalSeconds = judgeTime(endTime, startTime)
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
    User.objects.all().filter(inBlacklistTime=changeDate).update(inBlacklistTime=None, inBlacklist=False, defaults=0)

    # 添加场地占用事件
    addEvents = AddEvent.objects.all().filter(date=now_date)
    for addEvent in addEvents:
        if addEvent.state == 1 or addEvent.state == 2:
            continue
        myDurations = addEvent.court.duration_set.all().filter(date=now_date)
        for myDuration in myDurations:
            if judgeAddEvent(addEvent.startTime, addEvent.endTime, myDuration.startTime, myDuration.endTime):
                myDuration.openState = 0
                myDuration.save()
                addEvent.state = 2
                addEvent.save()

    # 将在有效期之外的违约记录设置为失效
    Default.objects.all().filter(date=changeDate).update(valid=False)
    print("Finished!")


def minute_task():
    # 判断违约并记录违约事件
    print("Start minute update...")
    myDate = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
    myTime = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%H:%M')
    reserveEvents = ReserveEvent.objects.filter(date=myDate, cancel=0)
    for reserveEvent in reserveEvents:
        if judgeTime(reserveEvent.startTime,
                     calculateTime(myTime, -600)) == 0 and reserveEvent.checked == 0:
            print("default!")
            reserveEvent.checked = 1
            reserveEvent.user.defaults += 1
            reserveEvent.save()
            default = Default(user=reserveEvent.user, date=myDate, time=myTime)
            default.save()
            if reserveEvent.user.defaults >= 3:
                reserveEvent.user.inBlacklistTime = myDate
                reserveEvent.user.inBlacklist = True
            reserveEvent.user.save()
        elif judgeTime(reserveEvent.startTime, calculateTime(myTime, 600)) == 0:
            print("You have a reserve event!")
            news = News(user=reserveEvent.user, date=myDate, time=myTime)
        elif judgeTime(reserveEvent.endTime, calculateTime(myTime, 600) == 0) and reserveEvent.leave == 0:
            print("You are going to leave!")
    print("Finished!")



'''
若代码已经部署到服务器上，在本机上运行后端时务必将以下四行注释掉，否则会更改服务器数据库
'''


# sched = Scheduler()
# sched.add_cron_job(daily_task, hour=0, minute=0)
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
            return Response({'error': 'Login failed'}, status=403)
        loginToken = md5(userId)
        obj.loginToken = loginToken
        obj.save()
        url = None
        if obj.image:
            url = obj.image.url
        return Response(
            {'message': 'ok', 'username': obj.username, 'image': url, 'loginToken': loginToken})


class LogoutView(APIView):
    """
    管理员注销
    """
    authentication_classes = [ManagerAuthtication]

    def post(self, request):
        manager = request.user
        manager.loginToken = ''
        manager.save()
        return Response({'message': 'ok'})


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
            return Response({'error': ser.errors}, 400)
        ser.update(request.user, ser.validated_data)
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


class StadiumView(ListAPIView, CreateAPIView):
    """
    场馆信息
    """
    # authentication_classes = [ManagerAuthtication]
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializerForManager
    filter_class = StadiumFilter

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST':
            return CreateStadiumSerializer(*args, **kwargs)
        return StadiumSerializerForManager(*args, **kwargs)

    def put(self, request):
        req_data = request.data
        ser = StadiumSerializerForManager(data=req_data)
        if not ser.is_valid():
            return Response({'error': ser.errors}, status=400)
        stadium = Stadium.objects.filter(id=ser.validated_data.get('stadium_id')).first()
        ser.update(stadium, ser.validated_data)
        return Response({'message': 'ok'})


class StadiumImageView(CreateAPIView):
    """
    场馆图片信息
    """
    # authentication_classes = [ManagerAuthtication]
    serializer_class = StadiumImageSerializer


class CourtTypeView(ListAPIView):
    """
    场地类型信息
    """
    queryset = CourtType.objects.all()
    serializer_class = CourtTypeSerializerForManager
    filter_class = CourtTypeFilter

    def post(self, request):
        req_data = request.data
        ser = CourtTypeSerializerForManager(data=req_data)
        if not ser.is_valid():
            return Response({'error': ser.errors}, status=400)
        number_ser = NumberSerializer(data=req_data)
        if not number_ser.is_valid():
            return Response({'error': number_ser.errors}, status=400)
        courtType = ser.save()
        num = number_ser.validated_data.get('num')
        for i in range(1, num + 1):
            Court.objects.create(stadium=courtType.stadium, courtType=courtType, price=courtType.price, openState=0,
                                 location='304B', type=courtType.type, name=courtType.type + str(i) + '号场地')
        return Response({'message': 'ok'})


class CourtView(ListAPIView):
    """
    场地信息
    """

    # authentication_classes = [ManagerAuthtication]
    queryset = Court.objects.all()
    serializer_class = CourtSerializer
    filter_class = CourtFilter


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
    serializer_class = ReserveEventSerializerForManager
    filter_class = ReserveEventFilter
    pagination_class = ReserveHistoryPagination

    def get_queryset(self):
        return ReserveEvent.objects.all().order_by('-createTime')


class CommentView(ListAPIView):
    """
    用户评论
    """
    authentication_classes = [ManagerAuthtication]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializerForManager
    filter_class = CommentFilter
    pagination_class = CommentPagination

    def get_queryset(self):
        return Comment.objects.all().order_by('-createTime')


class DefaultView(ListAPIView):
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
            return Response({'error': 'Invalid default_id'}, status=400)
        if default.cancel == 1:
            return Response({'error': 'manager has cancelled this record.'}, status=400)
        default.cancel = 1
        default.save()
        user = default.user
        user.defaults -= 1
        if user.defaults < 3:
            user.inBlacklist = 0
            user.inBlacklistTime = None
        user.save()
        return Response({'message': 'ok'})


class ChangeDurationView(ListAPIView, CreateAPIView):
    """
    修改预约时段信息
    """

    authentication_classes = [ManagerAuthtication]
    queryset = ChangeDuration.objects.all()
    serializer_class = ChangeDurationSerializer
    filter_class = ChangeDurationFilter

    def put(self, request):
        pass
        # TODO: 只接受一个参数id，并实现逻辑


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
            return Response({'error': ser.errors}, status=400)
        addEvent = ser.save(manager=request.user)
        startTime = addEvent.startTime
        endTime = addEvent.endTime
        myDurations = addEvent.court.duration_set.all().filter(date=addEvent.date)
        for myDuration in myDurations:
            if judgeAddEvent(startTime, myDuration.startTime, endTime, myDuration.endTime):
                myDuration.openState = 0
                myDuration.save()
                reserveEvent = ReserveEvent.objects.filter(duration_id=myDuration.id).first()
                if not reserveEvent:
                    continue
                # TODO: 最好在这里给用户发回一条消息
                reserveEvent.cancel = 1
                reserveEvent.save()
        return Response({'message': 'ok'})

    def put(self, request):
        pass
        # TODO: 只接受一个参数id，并实现逻辑


class AddBlacklistView(ListAPIView, CreateAPIView):
    """
    加入黑名单操作
    """
    authentication_classes = [ManagerAuthtication]
    queryset = AddBlacklist.objects.all()
    serializer_class = AddBlacklistSerializer
    filter_class = AddBlacklistFilter

    def put(self, request):
        req_data = request.data
        id = req_data.get('id')
        # TODO: 管理员可以撤销其他管理员的操作么？
        addBlacklist = AddBlacklist.objects.filter(id=id).first()
        if not addBlacklist:
            return Response({'error': 'Invalid Blacklist_id'}, status=400)
        addBlacklist.state = 1
        addBlacklist.save()
        user = addBlacklist.user
        user.inBlacklist = 0
        user.inBlacklistTime = None
        user.save()
        return Response({'message': 'ok'})


class HistoryView(APIView):
    """
    历史操作信息
    """
    # TODO: 至少要支持分页吧
    authentication_classes = [ManagerAuthtication]

    def get(self, request):
        manager = request.user
        req_data = request.query_params
        type = req_data.get('type')
        if type == '1':
            operations = manager.changeduration_set.all().order_by('-time')
        elif type == '2':
            operations = manager.addevent_set.all().order_by('-time')
        elif type == '3':
            operations = manager.addblacklist_set.all().order_by('-time')
        else:
            changeDuration = manager.changeduration_set.all()
            addEvent = manager.addevent_set.all()
            addBlackList = manager.addblacklist_set.all()
            operations = sorted(chain(changeDuration, addEvent, addBlackList), key=attrgetter('time'), reverse=True)
        operations = [model_to_dict(ope, fields=['time', 'type', 'id', 'state', 'details', 'content']) for ope in
                      operations]
        # 分页
        ser = HistorySerializer(data=req_data)
        if not ser.is_valid():
            return Response({'error': ser.errors}, status=400)
        pagination = MyPagination(max_page_size=30)
        operations = pagination.paginate(operations, page=ser.validated_data.get('page'),
                                         size=ser.validated_data.get('size'))
        return Response(operations)


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
            return Response({'error': ser.errors}, status=400)
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

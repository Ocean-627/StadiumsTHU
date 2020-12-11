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
        print(loginToken)
        obj.save()
        ret = Response(
            {'message': 'ok', 'loginToken': loginToken})
        ret.set_cookie('loginToken', loginToken)
        return ret


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
        addEvent = ser.save()
        startTime = addEvent.startTime
        endTime = addEvent.endTime
        myDurations = addEvent.court.duration_set.all().filter(date=addEvent.date)
        for myDuration in myDurations:
            cp1 = judgeTime(myDuration.endTime, startTime)
            cp2 = judgeTime(startTime, myDuration.startTime)
            cp3 = judgeTime(myDuration.endTime, endTime)
            cp4 = judgeTime(endTime, myDuration.startTime)
            flag = 0
            flag += cp1 > 0 and cp2 > 0
            flag += cp3 > 0 and cp4 > 0
            flag += cp2 < 0 and cp3 < 0
            flag += cp2 > 0 and cp3 > 0
            if flag > 0:
                myDuration.openState = 0
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


def refresh():
    print("ok")
    # myStadium = stadium
    # myStadium.openingHours = openHours
    # myStadium.openTime = openTime
    # myStadium.closeTime = closeTime
    # myStadium.duration = duration
    # myCourts = myStadium.court_set.all()
    # myDurations = myStadium.duration_set.all()
    #
    # # 删除更改时间段后的不合法时间段，该时间段的date属性应不早于startDate
    # for myDuration in myDurations:
    #     if judgeDate(str(myDuration.date), str(startDate)) >= 0:
    #         myDuration.delete()
    # startDate = str(datetime.datetime.strptime(startDate, '%Y-%m-%d')).split()[0]
    # foreDays = judgeDate(str(calculateDate(datetime.datetime.now().strftime('%Y-%m-%d'), myStadium.foreDays)),
    #                      startDate)
    # if foreDays < 0:
    #     return JsonResponse({'message': 'ok'})
    # openHours = openHours.split()
    #
    # for openHour in openHours:
    #     startTime, endTime = openHour.split('-')
    #     totalSeconds = judgeTime(endTime, startTime)
    #     seconds = judgeTime(duration, "00:00")
    #     if totalSeconds % seconds != 0:
    #         return JsonResponse({'error': 'can not make durations according to temp information'})
    #     else:
    #         for k in range(int(totalSeconds // seconds)):
    #             endTime = (datetime.datetime.strptime(str(startTime), "%H:%M") + datetime.timedelta(
    #                 seconds=seconds)).strftime('%H:%M')
    #             for i in range(foreDays + 1):
    #                 date = calculateDate(startDate, i)
    #                 for j in range(len(myCourts)):
    #                     myDuration = Duration(stadium=stadium, court=myCourts[j], startTime=startTime,
    #                                           endTime=endTime, date=date, openState=1, accessible=1)
    #                     myDuration.save()
    #             startTime = endTime


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

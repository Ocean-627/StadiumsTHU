from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from app.authtication import UserAuthtication
from app.serializer import *
from app.utils import *


class LogonView(APIView):
    """
    用户注册
    """
    def post(self, request):
        req_data = request.data
        # 校验输入
        ser = UserSerializer(data=req_data)
        if not ser.is_valid():
            return Response({'error': ser.errors})
        username = req_data.get('username')
        password = req_data.get('password')
        email = req_data.get('email')
        userId = req_data.get('userId')
        user = User(username=username, password=password, email=email, userId=userId)
        user.save()
        return Response({'message': 'ok'})


class LoginView(APIView):
    """
    用户登录
    """

    def post(self, request):
        req_data = request.data
        userId = req_data.get('userId')
        password = req_data.get('password')
        obj = User.objects.filter(userId=userId, password=password).first()
        if not obj:
            return Response({'error': 'Login failed'})
        loginToken = md5(userId)
        obj.loginToken = loginToken
        obj.save()
        return Response({'message': 'ok', 'loginToken': loginToken})


class StadiumView(APIView):
    """
    场馆信息
    """
    authentication_classes = [UserAuthtication]

    def get(self, request):
        stadiums = Stadium.objects.all()
        stadiums = StadiumSerializer(stadiums, many=True)
        return Response({'message': 'ok', 'stadiums': stadiums.data})


class CourtView(APIView):
    """
    场地信息
    """
    authentication_classes = [UserAuthtication]

    def get(self, request):
        req_data = request.query_params
        id = req_data.get('id')
        stadium = Stadium.objects.filter(id=id).first()
        if not stadium:
            return Response({'error': 'Stadium does not exist'})
        courts = stadium.court_set.all()
        courts = CourtSerializer(courts, many=True)
        return Response({'message': 'ok', 'courts': courts.data})


class DurationView(APIView):
    """
    时段信息
    """
    authentication_classes = [UserAuthtication]

    def get(self, request):
        req_data = request.query_params
        id = req_data.get('id')
        court = Court.objects.filter(id=id).first()
        if not court:
            return Response({'error': 'Court does not exist'})
        durations = court.duration_set.all()
        durations = DurationSerializer(durations, many=True)
        return Response({'message': 'ok', 'durations': durations.data})


class ReserveView(APIView):
    """
    预订信息
    """
    authentication_classes = [UserAuthtication]

    def get(self, request):
        # 获取预订信息
        user = request.user
        events = user.reserveevent_set.all()
        events = ReserveEventSerializer(events, many=True)
        return Response({'message': 'ok', 'history': events.data})

    def post(self, request):
        # 预定场地
        req_data = request.data
        durationId = req_data.get('durationId')
        duration = Duration.objects.filter(id=durationId).first()
        if not duration:
            return Response({'error': 'Invalid duration id'})
        user = request.user
        stadium = duration.stadium
        court = duration.court
        reserveevent = ReserveEvent(stadium=stadium, court=court, user=user, duration=duration, result='W',
                                    startTime=duration.startTime,
                                    endTime=duration.endTime)
        reserveevent.save()
        return JsonResponse({'message': 'ok', 'eventId':reserveevent.id})

    def delete(self, request):
        # 取消预订
        req_data = request.data
        eventId = req_data.get('eventId')
        event = ReserveEvent.objects.filter(id=eventId).first()
        if not event:
            return Response({'error': 'Reserve does not exist'})
        event.cancel = True
        # TODO:退款等操作
        return Response({'message': 'ok'})

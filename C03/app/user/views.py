from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.timezone import now

from app.utils.authtication import UserAuthtication
from app.utils.throttle import UserThrottle
from app.utils.filter import *
from app.utils.serializer import *
from app.utils.pagination import *
from app.utils.utils import *
from app.user import wx


class LoginView(APIView):
    """
    用户登录
    """

    def post(self, request):
        req_data = request.data
        code = req_data.get('code')
        if not code:
            return Response({'error': 'Requires code'})
        try:
            auth = wx.login(js_code=code)
            openId = auth.get('openid')
            if not openId:
                return Response({'error': 'Invalid code'})
            user = User.objects.filter(openId=openId).first()
            if not user:
                user = User(openId=openId)
                user.save()
            loginToken = md5(openId)
            user.loginToken = loginToken
            user.loginTime = now()
            user.save()
            return Response({'message': 'ok', 'loginToken': loginToken})
        except Exception as e:
            return Response({'error': 'Exception occurred'})


class UserView(APIView):
    """
    用户信息
    """
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]

    def get(self, request):
        user = request.user
        user = UserSerializer(user, many=False)
        return Response(user.data)

    def post(self, request):
        req_data = request.data
        ser = UserSerializer(data=req_data)
        if not ser.is_valid():
            return Response({'error': ser.errors})
        ser.update(request.user, ser.validated_data)
        return Response({'message': 'ok'})


class StadiumView(ListAPIView):
    """
    场馆信息
    """
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer
    filter_class = StadiumFilter


class CourtView(ListAPIView):
    """
    场地信息
    """
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]
    queryset = Court.objects.all()
    serializer_class = CourtSerializer
    filter_class = CourtFilter


class DurationView(ListAPIView):
    """
    时段信息
    """
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]
    queryset = Duration.objects.all()
    serializer_class = DurationSerializer
    filter_class = DurationFilter


class ReserveView(ListAPIView, CreateAPIView):
    """
    预订信息
    """
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]
    queryset = ReserveEvent.objects.all()
    serializer_class = ReserveEventSerializer
    filter_class = ReserveEventFilter

    def get_queryset(self):
        return ReserveEvent.objects.filter(user=self.request.user)

    def put(self, request):
        # 取消预订
        req_data = request.data
        user = request.user
        eventId = req_data.get('event_id')
        event = ReserveEvent.objects.filter(user=user, id=eventId).first()
        if not event:
            return Response({'error': 'Reserve does not exist'})
        event.cancel = True
        event.save()
        # TODO:进行退款等操作
        duration = Duration.objects.get(id=event.duration_id)
        duration.user = None
        duration.accessible = True
        duration.save()
        return Response({'message': 'ok'})

    def delete(self, request):
        return Response({'message': 'ok'})


class CommentView(ListAPIView, CreateAPIView):
    """
    评价场馆
    可以考虑重写get_serializer方法
    TODO:一次性批量提交图片
    """
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_class = CommentFilter

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def delete(self, request):
        req_data = request.data
        id = req_data.get('comment_id')
        user = request.user
        comment = user.comment_set.filter(user=user, id=id).first()
        if not comment:
            return Response({'error': 'Delete comment failed'})
        comment.delete()
        return Response({'message': 'ok'})


class CommentImageView(CreateAPIView):
    """
    评价对应的图片
    """
    authentication_classes = [UserAuthtication]
    serializer_class = CommentImageSerializer


class CollectView(ListAPIView, CreateAPIView):
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]
    queryset = CollectEvent.objects.all()
    serializer_class = CollectEventSerializer
    filter_class = CollectEventFilter

    def get_queryset(self):
        return CollectEvent.objects.filter(user=self.request.user)

    def delete(self, request):
        req_data = request.data
        id = req_data.get('collect_id')
        user = request.user
        collect = CollectEvent.objects.filter(user=user, id=id).first()
        if not collect:
            return Response({'error': 'Invalid collect_id'})
        collect.delete()
        return Response({'message': 'ok'})


class SessionView(ListAPIView, CreateAPIView):
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    filter_class = SessionFilter

    def get_queryset(self):
        return Session.objects.filter(user=self.request.user.id)


class MessageView(ListAPIView, CreateAPIView):
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_class = MessageFilter

    def get_queryset(self):
        sessions = Session.objects.filter(user=self.request.user.id)
        queryset = None
        for session in sessions:
            if not queryset:
                queryset = session.message_set.all()
            else:
                queryset = queryset | session.message_set.all()
        return queryset

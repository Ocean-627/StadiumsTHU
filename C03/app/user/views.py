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
from app.user import thss


class LoginView(APIView):
    """
    用户登录
    """

    def post(self, request):
        req_data = request.data
        token = req_data.get('token')
        if not token:
            return Response({'error': 'Requires token'})
        auth = thss.login(token=token).get('user')
        if not auth:
            return JsonResponse({'error': 'Login failed'})
        userId = auth.get('card')
        user = User.objects.filter(userId=userId).first()
        if not user:
            user = User(userId=userId, name=auth.get('name'), phone=auth.get('cell'), email=auth.get('mail'))
            user.save()
        loginToken = md5(userId)
        user.loginToken = loginToken
        user.save()
        return Response({'message': 'ok', 'loginToken': loginToken})


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


class StadiumDetailView(ListAPIView):
    """
    场馆详细信息
    """
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]
    queryset = Stadium.objects.all()
    serializer_class = StadiumDetailSerializer
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
    pagination_class = CommentPagination

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
    """
    收藏场馆
    """
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
    """
    会话信息
    """
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    filter_class = SessionFilter

    def get_queryset(self):
        return Session.objects.filter(user_id=self.request.user.id)

    def put(self, request):
        req_data = request.data
        session_id = req_data.get('session_id')
        session = Session.objects.filter(id=session_id, user_id=self.request.user.id).first()
        if not session:
            return Response({'error': 'Invalid session_id'})
        session.open = False
        session.save()
        return Response({'message': 'ok'})


class MessageView(ListAPIView, CreateAPIView):
    """
    消息
    """
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_class = MessageFilter

    def get_queryset(self):
        sessions = Session.objects.filter(user_id=self.request.user.id)
        queryset = None
        for session in sessions:
            if not queryset:
                queryset = session.message_set.all()
            else:
                queryset = queryset | session.message_set.all()
        return queryset

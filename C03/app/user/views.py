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
from app.utils.utils import *


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
        ser.save()
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
        obj.loginTime = now()
        obj.save()
        return Response({'message': 'ok', 'loginToken': loginToken})


class LogoutView(APIView):
    """
    用户登出
    """
    authentication_classes = [UserAuthtication]

    def post(self, request):
        user = request.user
        user.loginToken = ''
        user.save()
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
        eventId = req_data.get('eventId')
        event = ReserveEvent.objects.filter(user=user, id=eventId).first()
        if not event:
            return Response({'error': 'Reserve does not exist'})
        event.cancel = True
        event.save()
        # TODO:进行退款等操作
        duration = event.duration
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
        id = req_data.get('commentId')
        user = request.user
        comment = user.comment_set.filter(user=user, id=id).first()
        if not comment:
            return Response({'error': 'Delete comment failed'})
        comment.delete()
        return Response({'message': 'ok'})


class CommentImageView(APIView):
    """
    评价对应的图片
    #TODO:只在后端开发时测试用
    """
    authentication_classes = [UserAuthtication]

    def post(self, request):
        req_data = request.data
        commentId = req_data.get('comment_id')
        image = req_data.get('image')
        user = request.data
        comment = Comment.objects.filter(user=user, id=commentId).first()
        if not comment:
            return Response({'error': 'Comment does not exist'})
        item = CommentImage(comment=comment, image=image)
        item.save()
        return Response({'message': 'ok'})

    def get(self, request):
        req_data = request.query_params
        imageId = req_data.get('image_id')
        image = CommentImage.objects.filter(id=imageId).first()
        if not image:
            return Response({'error': 'Image does not exist'})
        return HttpResponse(image.image, content_type='image/jpeg')

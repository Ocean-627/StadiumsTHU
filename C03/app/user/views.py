from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
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


class ReserveView(APIView):
    """
    预订信息
    """
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]

    def get(self, request):
        # 获取预订信息
        # TODO:筛选
        user = request.user
        events = user.reserveevent_set.all()
        events = ReserveEventSerializer(events, many=True)
        return Response({'message': 'ok', 'history': events.data})

    def post(self, request):
        # 预定场地
        req_data = request.data
        durationId = req_data.get('durationId')
        duration = Duration.objects.filter(id=durationId, accessible=True).first()
        if not duration:
            return Response({'error': 'Reserve failed'})
        user = request.user
        stadium = duration.stadium
        court = duration.court
        # 不允许重复预订
        obj = ReserveEvent.objects.filter(id=durationId, user=user, result='W').first()
        if obj:
            return Response({'error': 'Same reverse has applied'})
        reserveevent = ReserveEvent(stadium=stadium, court=court, user=user, duration=duration, result='W',
                                    startTime=duration.startTime,
                                    endTime=duration.endTime)
        reserveevent.save()
        return JsonResponse({'message': 'ok', 'eventId': reserveevent.id})

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


class CommentView(APIView):
    """
    评价场馆
    """
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]

    def post(self, request):
        req_data = request.data
        user = request.user
        courtId = req_data.get('courtId')
        court = Court.objects.filter(id=courtId).first()
        if not court:
            return Response({'error': 'Court does not exist'})
        content = req_data.get('content')
        if not content:
            return Response({'error': 'Empty content'})
        comment = Comment(user=user, court=court, content=content)
        comment.save()
        return Response({'message': 'ok', 'commentId': comment.id})

    def get(self, request):
        user = request.user
        comments = user.comment_set.all()
        comments = CommentSerializer(comments, many=True)
        return Response({'message': 'ok', 'comments': comments.data})

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
        commentId = req_data.get('commentId')
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
        imageId = req_data.get('imageId')
        image = CommentImage.objects.filter(id=imageId).first()
        if not image:
            return Response({'error': 'Image does not exist'})
        return HttpResponse(image.image, content_type='image/jpeg')

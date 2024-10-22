from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.timezone import now

from app.utils.authtication import UserAuthtication
from app.utils.permission import UserPermission
from app.utils.throttle import UserThrottle
from app.utils.filter import *
from app.utils.user_serializer import *
from app.utils.pagination import *
from app.utils.utils import *
from app.user import thss
from app.user import wx


class LoginView(APIView):
    """
    用户登录
    """

    def post(self, request):
        req_data = request.data
        # 从身份认证程序获取信息
        token = req_data.get('token')
        if not token:
            return Response({'error': 'Requires token'}, status=400)
        auth = thss.login(token=token).get('user')
        if not auth:
            return JsonResponse({'error': 'Login failed because something wrong with authtication_app'}, status=500)
        userId = auth.get('card')
        # 从微信后端获取openid
        js_code = req_data.get('js_code')
        if not js_code:
            return Response({'error': 'Requires js_code'}, status=400)
        resp = wx.login(js_code)
        openId = resp.get('openid')
        if not openId:
            return Response({'error': 'Login failed because something wrong with weixin_app'}, status=500)
        # 创建用户
        user = User.objects.filter(userId=userId).first()
        if not user:
            user = User.objects.create(userId=userId, nickName=auth.get('name'), name=auth.get('name'),
                                       phone=auth.get('cell'), openId=openId,
                                       email=auth.get('mail'), major=auth.get('department'))
        loginToken = md5(userId)
        user.loginToken = loginToken
        user.openId = openId
        user.save()
        return Response({'message': 'ok', 'loginToken': loginToken})


class LogoutView(APIView):
    """
    登出
    """
    authentication_classes = [UserAuthtication]

    def post(self, request):
        user = self.request.user
        user.loginToken = ''
        user.save()
        return Response({'message': 'ok'})


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
            return Response({'error': ser.errors}, status=400)
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


class CourtTypeView(APIView):
    """
    全部运动类型
    """
    authentication_classes = [UserAuthtication]
    throttle_classes = [UserThrottle]

    def get(self, request):
        types = CourtType.objects.values('type').distinct()
        res = [item['type'] for item in types]
        return Response(res)


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


class BatchReserveView(CreateAPIView):
    """
    批量预订，只支持POST方法
    """
    authentication_classes = [UserAuthtication]
    permission_classes = [UserPermission]
    serializer_class = BatchReserveSerializer


class ReserveView(ListAPIView, CreateAPIView):
    """
    预订信息
    """
    authentication_classes = [UserAuthtication]
    permission_classes = [UserPermission]
    throttle_classes = [UserThrottle]
    queryset = ReserveEvent.objects.all()
    serializer_class = ReserveEventSerializer
    filter_class = ReserveEventFilter
    pagination_class = ReserveHistoryPagination

    def get_queryset(self):
        return ReserveEvent.objects.filter(user=self.request.user).order_by('-createTime')

    def put(self, request):
        req_data = request.data
        ser = ReserveModifySerializer(data=req_data)
        if not ser.is_valid():
            return Response({'error': ser.errors}, status=400)
        reserve = ReserveEvent.objects.get(id=ser.validated_data.get('id'))
        ser.update(reserve, ser.validated_data)
        # 额外处理退订事件
        if ser.validated_data.get('cancel'):
            duration = Duration.objects.filter(id=reserve.duration_id).first()
            if not duration:
                return Response({'error': 'Duration not found'}, status=404)
            date = duration.date
            # TODO: 只根据日期判断，暂定为2天
            cur = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
            if judgeDate(date, cur) < 2:
                return Response({'error': 'You can not cancel this reserve because it will due in 2 days.'}, status=400)
            # 发送取消成功
            content = '您的预定取消成功'
            News.objects.create(user=request.user, type='预约取消', content=content)
            wx.reserve_cancel_message(openId=request.user.openId, type=duration.court.type, date=duration.date,
                                      content=content)
            # 更改预订状态
            court = duration.court
            startTime = reserve.startTime
            endTime = reserve.endTime
            for myDuration in court.duration_set.filter(date=duration.date):
                if judgeAddEvent(startTime, myDuration.startTime, endTime, myDuration.endTime):
                    myDuration.user = None
                    myDuration.accessible = True
                    myDuration.save()

        return Response({'message': 'ok'})

    def delete(self, request):
        req_data = request.data
        id = req_data.get('id')
        reserve = ReserveEvent.objects.filter(id=id, user=request.user).first()
        if not reserve:
            return Response({'error': '预约不存在'}, status=400)
        if not reserve.cancel and not reserve.leave:
            return Response({'error': '预约正在进行中，无法删除'}, status=400)
        reserve.delete()
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
        req_data = self.request.query_params
        selfOnly = req_data.get('selfOnly')
        if selfOnly:
            return Comment.objects.filter(user=self.request.user)
        return Comment.objects.all()

    def delete(self, request):
        req_data = request.data
        id = req_data.get('comment_id')
        user = request.user
        comment = user.comment_set.filter(user=user, id=id).first()
        if not comment:
            return Response({'error': 'Delete comment failed'}, status=400)
        reserve = ReserveEvent.objects.filter(id=comment.reserve_id).first()
        comment.delete()
        if reserve:
            num = len(Comment.objects.filter(reserve_id=reserve.id))
            if not num:
                reserve.has_comments = False
                reserve.save()
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
    pagination_class = CollectPagination

    def get_queryset(self):
        return CollectEvent.objects.filter(user=self.request.user)

    def delete(self, request):
        req_data = request.data
        id = req_data.get('collect_id')
        user = request.user
        collect = CollectEvent.objects.filter(user=user, id=id).first()
        if not collect:
            return Response({'error': 'Invalid collect_id'}, status=400)
        collect.delete()
        return Response({'message': 'ok'})


class NewsView(ListAPIView):
    """
    消息，目前只使用这个版本，即后端自动生成消息，用户可以查看但不能发送给系统
    """
    authentication_classes = [UserAuthtication]
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_class = NewsFilter
    pagination_class = NewsPagination

    def get_queryset(self):
        return News.objects.filter(user=self.request.user).order_by('-createTime')

    def put(self, request):
        req_data = request.data
        id = req_data.get('id')
        news = News.objects.filter(user=request.user, id=id).first()
        if not news:
            return Response({'error': 'Invalid id'}, status=400)
        news.checked = True
        news.save()
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
            return Response({'error': 'Invalid session_id'}, status=400)
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

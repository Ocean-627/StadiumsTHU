from django.db import models
from app.utils.validator import *
import django.utils.timezone as timezone


# Create your models here.
class User(models.Model):
    # 普通用户
    loginToken = models.CharField(max_length=100, null=True)
    loginTime = models.DateTimeField(auto_now=True, null=True)
    type = models.CharField(max_length=10, default='在校学生')
    name = models.CharField(max_length=32, null=True)
    nickName = models.CharField(max_length=32, null=True)
    userId = models.IntegerField(verbose_name='学生编号', unique=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20, null=True)
    major = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='user', verbose_name='头像', null=True)
    defaults = models.IntegerField(verbose_name='违约次数', default=0)
    blacklist = models.CharField(max_length=20, null=True)
    # TODO:完善信息


class Stadium(models.Model):
    # 场馆
    name = models.CharField(max_length=32)
    pinyin = models.CharField(max_length=100, null=True)
    information = models.CharField(max_length=300)
    # TODO:开放时间和关闭时间可以设置为DateField
    openTime = models.CharField(max_length=32)
    closeTime = models.CharField(max_length=32)
    contact = models.CharField(max_length=32, null=True)
    openState = models.BooleanField()
    foreDays = models.IntegerField()
    durations = models.CharField(max_length=32, null=True)
    location = models.CharField(max_length=10, null=True, default="学堂路")
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, verbose_name='经度')
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, verbose_name='纬度')
    # TODO:完善信息


class Manager(models.Model):
    # 场馆管理员
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    userId = models.IntegerField(verbose_name='管理员编号', unique=True)
    email = models.EmailField()
    loginToken = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='manager', verbose_name='头像', null=True)
    # TODO:完善信息


class CourtType(models.Model):
    # 类型信息(某个场馆）
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    openingHours = models.CharField(max_length=50, verbose_name='开放时间')
    type = models.CharField(max_length=20, verbose_name='场馆类型')
    duration = models.CharField(max_length=30, verbose_name='单次预约限定时长', default="01:00")
    price = models.IntegerField(verbose_name='预约费用', default=30)
    membership = models.IntegerField(verbose_name='同行人数', default=3)
    openState = models.BooleanField()


class Court(models.Model):
    # 场地
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    courtType = models.ForeignKey(CourtType, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, verbose_name='场馆类型')
    name = models.CharField(max_length=32, null=True)
    price = models.IntegerField()
    openState = models.BooleanField()
    floor = models.IntegerField(null=True)
    location = models.CharField(max_length=100)
    # TODO:完善信息


class ReserveEvent(models.Model):
    SUCCESS = 'S'
    FAIL = 'F'
    WAITING = 'W'
    APPLY_RESULT = (
        (SUCCESS, 'success'),
        (FAIL, 'fail'),
        (WAITING, 'waiting'),
    )
    # 预定事件
    stadium = models.CharField(max_length=32)
    stadium_id = models.IntegerField()
    court = models.CharField(max_length=32)
    court_id = models.IntegerField()
    duration_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.CharField(max_length=2, choices=APPLY_RESULT, default=WAITING, verbose_name='预定结果')
    date = models.CharField(max_length=10)
    startTime = models.CharField(max_length=50)
    endTime = models.CharField(max_length=50)
    payment = models.BooleanField(default=False, verbose_name='是否支付')
    cancel = models.BooleanField(default=False, verbose_name='是否取消')
    checked = models.BooleanField(default=False, verbose_name='是否使用')
    leave = models.BooleanField(default=False, verbose_name='是否离开')
    # TODO:完善事件信息


class Duration(models.Model):
    # 预约时段
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    courtType = models.ForeignKey(CourtType, related_name='+', on_delete=models.CASCADE, null=True)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.CharField(max_length=10)
    startTime = models.CharField(max_length=10)
    endTime = models.CharField(max_length=10)
    openState = models.BooleanField()
    accessible = models.BooleanField()


class ChangeDuration(models.Model):
    # （永久）修改预约时段事件
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    courtType = models.ForeignKey(CourtType, on_delete=models.CASCADE)
    openingHours = models.CharField(max_length=300)
    duration = models.CharField(max_length=10, null=True)
    date = models.CharField(max_length=32)
    time = models.DateTimeField(default=timezone.now)
    type = models.CharField(default="修改预约时间段", max_length=20)
    price = models.IntegerField(default=1)
    membership = models.IntegerField(default=1)
    openState = models.BooleanField()
    details = models.CharField(default="计算机网络", max_length=100)
    content = models.CharField(default="软件工程", max_length=100)
    state = models.IntegerField()
    # TODO:完善事件信息


class ChangeSchedule(models.Model):
    # 修改场馆开放和关闭时间点
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    openState = models.BooleanField()
    openTime = models.CharField(max_length=30)
    closeTime = models.CharField(max_length=30)
    startDate = models.CharField(max_length=30)
    foreDays = models.IntegerField()


class AddEvent(models.Model):
    # （临时）添加活动事件
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    startTime = models.CharField(max_length=32)
    endTime = models.CharField(max_length=32)
    date = models.CharField(max_length=32)
    time = models.DateTimeField(default=timezone.now)
    type = models.CharField(default="场地占用", max_length=20)
    information = models.CharField(max_length=1000, null=True)
    details = models.CharField(default="汇编与编译原理", max_length=100)
    content = models.CharField(default="软件工程", max_length=100)
    state = models.IntegerField()
    # TODO:完善事件信息


class Comment(models.Model):
    # 场地评论
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    stadium_id = models.IntegerField()
    reserve_id = models.IntegerField()
    score = models.IntegerField(default=3)
    content = models.CharField(max_length=300)


class CommentImage(models.Model):
    # 评论图片
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='comment')


class StadiumImage(models.Model):
    # 场馆图片
    # TODO:解决如何导入场馆信息的问题
    detail = models.CharField(max_length=30, verbose_name='图片描述', null=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stadium')


class CollectEvent(models.Model):
    # 收藏信息
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)


class Session(models.Model):
    # 会话
    user_id = models.IntegerField()
    open = models.BooleanField(default=True, verbose_name='会话状态')
    checked = models.BooleanField(default=False, verbose_name='审核状态')
    createTime = models.DateTimeField(auto_now_add=True)
    # 最近更新时间
    updateTime = models.DateTimeField(auto_now=True)


class Message(models.Model):
    # 消息
    USER = 'U'
    MANAGER = 'M'
    SENDER = (
        (USER, 'user'),
        (MANAGER, 'manager'),
    )
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    sender = models.CharField(max_length=2, choices=SENDER, verbose_name='发送方')
    # 如果sender为MANGER 则需要保存manager的id
    manager_id = models.IntegerField(null=True)
    content = models.CharField(max_length=500)
    createTime = models.DateTimeField(auto_now_add=True)


class Default(models.Model):
    # 违约记录
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    cancel = models.BooleanField(default=False, verbose_name='管理员是否手动撤销预约记录')
    detail = models.CharField(max_length=20, default="预约不来")
    valid = models.BooleanField(default=True, verbose_name='违约记录是否在有效期之内')
    # TODO:完善信息


class AddBlacklist(models.Model):
    # 添加至黑名单操作
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(default="移入黑名单", max_length=20)
    time = models.DateTimeField(default=timezone.now)
    details = models.CharField(default="操作系统", max_length=100)
    content = models.CharField(default="软件工程", max_length=100)
    state = models.IntegerField()
    # TODO:完善信息


class OtherOperation(models.Model):
    # 其他不可撤销操作，主要包括移出黑名单操作，撤销信用记录操作及编辑场馆信息操作
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    type = models.CharField(default="其他操作", max_length=20)
    details = models.CharField(default="软件工程", max_length=100)
    content = models.CharField(default="软件工程", max_length=100)
    # TODO:完善信息

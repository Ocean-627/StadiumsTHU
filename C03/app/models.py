from django.db import models
from app.utils.validator import *
import django.utils.timezone as timezone


# Create your models here.
class User(models.Model):
    # 普通用户
    openId = models.CharField(max_length=50, unique=True)
    loginToken = models.CharField(max_length=100, null=True)
    loginTime = models.DateTimeField(auto_now=True, null=True)
    # TODO:通过身份验证或用户完善信息的方式获取以下fields
    auth = models.BooleanField(default=False)
    name = models.CharField(max_length=32, null=True)
    nickName = models.CharField(max_length=32, null=True)
    userId = models.IntegerField(verbose_name='学生编号', null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20, null=True)
    # TODO:完善信息


class Stadium(models.Model):
    # 场馆
    name = models.CharField(max_length=32)
    pinyin = models.CharField(max_length=100)
    information = models.CharField(max_length=300)
    # TODO:开放时间和关闭时间可以设置为DateField
    openTime = models.CharField(max_length=32)
    closeTime = models.CharField(max_length=32)
    contact = models.CharField(max_length=32, null=True)
    openState = models.BooleanField()
    foreDays = models.IntegerField()
    durations = models.CharField(max_length=32, null=True)
    score = models.FloatField(verbose_name='评分', default=4.9)
    comments = models.IntegerField(default=0)
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
    # TODO:完善信息


class CourtType(models.Model):
    # 类型信息(某个场馆）
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    openingHours = models.CharField(max_length=50, verbose_name='开放时间')
    type = models.CharField(max_length=20, verbose_name='场馆类型')
    duration = models.CharField(max_length=30, verbose_name='单次预约限定时长', default="01:00")
    price = models.IntegerField(verbose_name='预约费用', default=30)
    membership = models.IntegerField(verbose_name='同行人数', default=3)


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


class Duration(models.Model):
    # 预约时段
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.CharField(max_length=10)
    startTime = models.CharField(max_length=10)
    endTime = models.CharField(max_length=10)
    openState = models.BooleanField()
    accessible = models.BooleanField()


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
    stadium = models.ForeignKey(Stadium, on_delete=models.DO_NOTHING)
    court = models.ForeignKey(Court, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.ForeignKey(Duration, on_delete=models.DO_NOTHING)
    result = models.CharField(max_length=2, choices=APPLY_RESULT, default=WAITING, verbose_name='预定结果')
    # TODO:开始时间和结束时间可以处理掉
    startTime = models.CharField(max_length=50)
    endTime = models.CharField(max_length=50)
    payment = models.BooleanField(null=True, verbose_name='是否支付')
    cancel = models.BooleanField(null=True, verbose_name='是否取消')
    checked = models.BooleanField(null=True, verbose_name='是否使用')
    leave = models.BooleanField(null=True, verbose_name='是否离开')
    # TODO:完善事件信息


class ChangeDuration(models.Model):
    # （永久）修改预约时段事件
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    openingHours = models.CharField(max_length=300)
    date = models.CharField(max_length=32)
    time = models.DateTimeField(default=timezone.now)
    type = models.IntegerField(default=1)
    # TODO:完善事件信息


class ChangeSchedule(models.Model):
    # 修改场馆开放和关闭时间点
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
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
    type = models.IntegerField(default=2)
    # TODO:完善事件信息


class Comment(models.Model):
    # 场地评论
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    score = models.IntegerField(default=3)
    content = models.CharField(max_length=300)


class CommentImage(models.Model):
    # 评论图片
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/%Y/%m/%d')


class UserImage(models.Model):
    # 用户图片
    # TODO:提供接口让用户提交图片
    detail = models.CharField(max_length=30, verbose_name='图片描述', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/user')


class StadiumImage(models.Model):
    # 场馆图片
    # TODO:解决如何导入场馆信息的问题
    detail = models.CharField(max_length=30, verbose_name='图片描述', null=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/stadium')

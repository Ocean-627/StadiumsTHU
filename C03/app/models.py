from django.db import models
from app.utils.validator import *
import django.utils.timezone as timezone


# Create your models here.
class User(models.Model):
    # 普通用户
    openId = models.CharField(max_length=50, null=True)
    loginToken = models.CharField(max_length=100, null=True)
    loginTime = models.DateTimeField(auto_now=True, null=True)
    # TODO:通过身份验证或用户完善信息的方式获取以下fields
    name = models.CharField(max_length=32, null=True)
    userId = models.IntegerField(verbose_name='学生编号', null=True, unique=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20, null=True)
    # TODO:完善信息


class Stadium(models.Model):
    # 场馆
    name = models.CharField(max_length=32)
    information = models.CharField(max_length=300)
    openingHours = models.CharField(max_length=50, verbose_name='开放时间')
    # TODO:开放时间和关闭时间可以设置为DateField
    openTime = models.CharField(max_length=32)
    closeTime = models.CharField(max_length=32)
    contact = models.CharField(max_length=32, null=True)
    openState = models.BooleanField()
    foreDays = models.IntegerField()
    durations = models.CharField(max_length=32, null=True)
    # TODO:完善信息


class Manager(models.Model):
    # 场馆管理员
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    userId = models.IntegerField(verbose_name='管理员编号', unique=True)
    email = models.EmailField()
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    loginToken = models.CharField(max_length=100, null=True)
    # TODO:完善信息


class Court(models.Model):
    # 场地
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
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
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
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
    content = models.CharField(max_length=300)


class CommentImage(models.Model):
    # 评论图片
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/%Y/%m/%d')


class UserImage(models.Model):
    # 用户图片
    # TODO:提供接口让用户提交图片
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/user')


class StadiumImage(models.Model):
    # 场馆图片
    # TODO:解决如何导入场馆信息的问题
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/stadium')

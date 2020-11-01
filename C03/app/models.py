from django.db import models


# Create your models here.
class User(models.Model):
    # 普通用户
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    userId = models.IntegerField()
    email = models.EmailField()
    loginToken = models.CharField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    # TODO:加入未读通知列表和违规次数


class Manager(models.Model):
    # 场馆管理员
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    userId = models.IntegerField()
    email = models.EmailField()
    workPlace = models.CharField(max_length=32, null=True)
    workPlaceId = models.IntegerField(null=True)
    loginToken = models.CharField(max_length=100)
    # TODO:加入未读通知列表


class Stadium(models.Model):
    # 场馆
    name = models.CharField(max_length=32)
    information = models.CharField(max_length=300)
    openingHours = models.CharField(max_length=50)
    # TODO:开放时间和关闭时间可以设置为DateField
    openTime = models.CharField(max_length=32)
    closeTime = models.TimeField(max_length=32)
    contact = models.IntegerField(null=True)
    openState = models.BooleanField()
    foreDays = models.IntegerField()
    # TODO:加入位置


class Court(models.Model):
    # 场地
    stadium = models.CharField(max_length=32)
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=32, null=True)
    price = models.IntegerField()
    openingHours = models.CharField(max_length=50)
    close = models.BooleanField()
    # TODO:加入位置,临时关闭时间


class Duration(models.Model):
    # 预约时段
    stadium = models.CharField(max_length=32)
    court = models.CharField(max_length=32, null=True)
    date = models.CharField(max_length=10)
    startTime = models.CharField(max_length=10)
    endTime = models.CharField(max_length=10)
    close = models.BooleanField()
    accessible = models.BooleanField()


class ReserveEvent(models.Model):
    # 预定事件
    stadiumId = models.IntegerField()
    stadiumName = models.CharField(max_length=32)
    courtId = models.IntegerField()
    courtName = models.CharField(max_length=32, null=True)
    result = models.BooleanField()
    startTime = models.CharField(max_length=50)
    endTime = models.CharField(max_length=50)
    payment = models.BooleanField()
    cancel = models.BooleanField()
    checked = models.BooleanField()
    leave = models.BooleanField()
    # TODO:完善事件信息

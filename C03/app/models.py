from django.db import models


# Create your models here.
class User(models.Model):
    # 普通用户
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    userId = models.IntegerField()
    loginToken = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone = models.IntegerField(null=True)
    # TODO:加入未读通知列表和违规次数


class Manager(models.Model):
    # 场馆管理员
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    userId = models.IntegerField()
    workPlace = models.CharField(max_length=32)
    workPlaceId = models.IntegerField()
    loginToken = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    # TODO:加入未读通知列表和违规次数



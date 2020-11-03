from django.db import models


# Create your models here.
class User(models.Model):
    # 普通用户
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    userId = models.IntegerField(verbose_name='studentId')
    email = models.EmailField()
    loginToken = models.CharField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    # TODO:完善信息


class Manager(models.Model):
    # 场馆管理员
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    userId = models.IntegerField(verbose_name='managerId')
    email = models.EmailField()
    workPlace = models.CharField(max_length=32, null=True)
    workPlaceId = models.IntegerField(null=True)
    loginToken = models.CharField(max_length=100)
    # TODO:完善信息


class Stadium(models.Model):
    # 场馆
    name = models.CharField(max_length=32)
    information = models.CharField(max_length=300)
    openingHours = models.CharField(max_length=50, verbose_name='scheduleForCourt')
    # TODO:开放时间和关闭时间可以设置为DateField
    openTime = models.CharField(max_length=32)
    closeTime = models.CharField(max_length=32)
    contact = models.CharField(max_length=32, null=True)
    openState = models.BooleanField()
    foreDays = models.IntegerField()
    schedule = models.CharField(max_length=32, null=True)
    # TODO:完善信息


class Court(models.Model):
    # 场地
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=32, null=True)
    price = models.IntegerField()
    openingHours = models.CharField(max_length=50)
    openState = models.BooleanField()
    # TODO:完善信息


class Duration(models.Model):
    # 预约时段
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
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
    stadiumName = models.CharField(max_length=32)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    courtName = models.CharField(max_length=32, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.ForeignKey(Duration, on_delete=models.CASCADE)
    result = models.CharField(max_length=2, choices=APPLY_RESULT, default=WAITING)
    startTime = models.CharField(max_length=50)
    endTime = models.CharField(max_length=50)
    payment = models.BooleanField(null=True, verbose_name='Whether user has payed')
    cancel = models.BooleanField(null=True, verbose_name='Whether this event has been canceled')
    checked = models.BooleanField(null=True, verbose_name='Whether user has used court')
    leave = models.BooleanField(null=True, verbose_name='Whether user has left court')
    # TODO:完善事件信息


class ChangeDuration(models.Model):
    # （永久）修改预约时段事件
    stadiumId = models.IntegerField()
    openingHours = models.CharField(max_length=300)
    date = models.CharField(max_length=32)
    # TODO:完善事件信息

"""
In this file we implement helper functions
"""
from app.models import *
from django.forms.models import model_to_dict
from datetime import datetime
import datetime


def md5(seq):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(seq, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


stadiums = [
    {'name': 'xxh的场馆',
     'pinyin': 'xxh',
     'information': 'xxh用来debug的场馆',
     'openTime': '08:00',
     'closeTime': '18:00',
     'contact': '4008823823',
     'openState': True,
     'foreDays': 3,
     'durations': '01:00'
     },
    {'name': 'cbx的场馆',
     'pinyin': 'cbx',
     'information': 'cbx用来写bug的场馆',
     'openTime': '07:00',
     'closeTime': '18:00',
     'contact': '18801225328',
     'openState': True,
     'foreDays': 2,
     'durations': '02:00'
     }
]


def initStadium(info):
    # 创建场馆
    Stadium.objects.create(**info)
    stadium = Stadium.objects.get(name=info['name'])
    # 创建场地类型
    type1 = CourtType(stadium=stadium, type='羽毛球', openingHours="8:00-10:00,13:00-17:00", openState=True)
    type1.save()
    type2 = CourtType(stadium=stadium, type='篮球', openingHours='8:00-10:00,13:00-17:00', openState=True)
    type2.save()
    # 创建场地
    courtNum = 5
    for i in range(courtNum):
        court1 = Court(stadium=stadium, courtType=type1, type=type1.type, name='场地' + str(i), price=30,
                       openState=stadium.openState, floor=1, location='110B')
        court1.save()
        court2 = Court(stadium=stadium, courtType=type2, type=type2.type, name='场地' + str(i), price=30,
                       openState=stadium.openState, floor=2, location='304B')
        court2.save()
        # 创建时段
        for t in range(10, 18):
            duration = Duration(stadium=stadium, court=court1, date='11.16', startTime=str(t) + ':00',
                                endTime=str(t + 1) + ':00', openState=True, accessible=True)
            duration.save()
            duration = Duration(stadium=stadium, court=court2, date='11.16', startTime=str(t) + ':00',
                                endTime=str(t + 1) + ':00', openState=True, accessible=True)
            duration.save()


def clearDatabase():
    # 清空场馆相关信息
    Stadium.objects.all().delete()


def judgeDate(A, B):
    # 判断A日期在B日期之后的天数
    format_pattern = '%Y-%m-%d'
    difference = (datetime.datetime.strptime(A, format_pattern) - datetime.datetime.strptime(B, format_pattern))
    return difference.days


def calculateDate(A, B):
    # 返回A日期B天之后的日期
    dateTime_p = datetime.datetime.strptime(A, '%Y-%m-%d')
    return (dateTime_p + datetime.timedelta(days=+B)).strftime("%Y-%m-%d")


def calculateTime(A, B):
    # 返回A时刻B秒之后的时刻
    dateTime_p = datetime.datetime.strptime(A, '%H:%M')
    return (dateTime_p + datetime.timedelta(seconds=+B)).strftime("%H:%M")


def judgeTime(A, B):
    # 判断A时刻在B时刻之后的秒数
    format_pattern = '%H:%M'
    difference = (datetime.datetime.strptime(A, format_pattern) - datetime.datetime.strptime(B, format_pattern))
    return difference.total_seconds()


def judgeAddEvent(event_start_time, duration_start_time, event_end_time, duration_end_time):
    # 判断事件是否会占用该时段
    cp1 = judgeTime(duration_end_time, event_start_time)
    cp2 = judgeTime(event_start_time, duration_start_time)
    cp3 = judgeTime(duration_end_time, event_end_time)
    cp4 = judgeTime(event_end_time, duration_start_time)
    flag = 0
    flag += cp1 > 0 and cp2 > 0
    flag += cp3 > 0 and cp4 > 0
    flag += cp2 < 0 and cp3 < 0
    flag += cp2 > 0 and cp3 > 0
    return flag > 0
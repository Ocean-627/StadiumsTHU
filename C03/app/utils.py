"""
In this file we implement helper functions
"""
from app.models import *
from django.forms.models import model_to_dict

stadiums = [
    {'name': 'xxh的场馆',
     'information': 'xxh用来debug的场馆',
     'openingHours': '8-12,14-18',
     'openTime': '8:00',
     'closeTime': '18:00',
     'contact': '4008823823',
     'openState': True,
     'foreDays': 3
     },
    {'name': 'cbx的场馆',
     'information': 'cbx用来写bug的场馆',
     'openingHours': '7-11,15-18',
     'openTime': '7:00',
     'closeTime': '18:00',
     'contact': '18801225328',
     'openState': True,
     'foreDays': 2
     }
]


def initStadium(stadium):
    # 创建场馆
    Stadium.objects.create(**stadium)
    # 创建场地
    courtNum = 5
    for i in range(courtNum):
        court = Court(stadium=stadium['name'], type='羽毛球', name='场地' + str(i), price=30,
                      openingHours=stadium['openingHours'], openState=stadium['openState'])
        court.save()
        # 创建时段
        openingHours = court.openingHours.split(',')
        t1, t2 = openingHours[0].split('-')
        t1, t2 = int(t1), int(t2)
        for t in range(t1, t2):
            duration = Duration(stadium=court.stadium, court=court.name, date='11.1', startTime=str(t),
                                endTime=str(t + 1), openState=True, accessible=True)
            duration.save()
        t1, t2 = openingHours[1].split('-')
        t1, t2 = int(t1), int(t2)
        for t in range(t1, t2):
            duration = Duration(stadium=court.stadium, court=court.name, date='11.1', startTime=str(t),
                                endTime=str(t + 1), openState=True, accessible=True)
            duration.save()


def clearDatabase():
    # 清空场馆相关信息
    Stadium.objects.all().delete()
    Court.objects.all().delete()
    Duration.objects.all().delete()


def json(vec):
    # 转化为json格式
    return [model_to_dict(item) for item in vec]
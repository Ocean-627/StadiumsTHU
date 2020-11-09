from django.http import JsonResponse
import hashlib
from itertools import chain
from operator import attrgetter
from app.utils import *


def logon(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    userId = request.POST.get('userId', '')
    # TODO:额外定义函数进行参数检查，这里只检查了不为空
    if not username or not password or not email or not userId:
        return JsonResponse({'error': 'Incomplete information'})
    manager = Manager(username=username, password=password, email=email, userId=userId)
    manager.save()
    return JsonResponse({'message': 'ok'})


def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    userId = request.POST.get('userId', '')
    password = request.POST.get('password', '')
    try:
        managerInfo = Manager.objects.get(userId=userId)
        # 已经登录
        if 'loginToken' in request.COOKIES:
            loginToken = request.COOKIES['loginToken']
            if loginToken == managerInfo.loginToken:
                return JsonResponse({'message': 'ok'})
        if password != managerInfo.password:
            return JsonResponse({'error': 'Wrong password'})
        # TODO:使用更合理的session算法
        loginToken = hashlib.sha1(userId.encode('utf-8')).hexdigest()
        managerInfo.loginToken = loginToken
        managerInfo.save()
        resp = JsonResponse({'message': 'ok'})
        # 设置Cookie
        resp.set_cookie('loginToken', loginToken)
        return resp
    except Manager.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'})


def logout(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    if 'loginToken' not in request.COOKIES:
        return JsonResponse({'error': 'Not yet logged in'})
    loginToken = request.COOKIES['loginToken']
    managerInfo = Manager.objects.get(loginToken=loginToken)
    managerInfo.loginToken = ''
    managerInfo.save()
    resp = JsonResponse({'message': 'ok'})
    resp.delete_cookie('loginToken')
    return resp


def get_court(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Requires GET'})
    workplace = request.GET.get('stadiumId', '')
    floor = request.GET.get('floor', '')
    date = request.GET.get('date', '')
    if not workplace or not floor or not date:
        return JsonResponse({'error': 'Incomplete information'})
    stadium = Stadium.objects.all().filter(id=int(workplace))[0]
    courts = stadium.court_set.all()
    courts = courts.filter(floor=floor)
    myCourts = []
    response = {"floor": floor, "number": len(courts), "duration": stadium.durations, "court": myCourts}
    for court in courts:
        myCourt = {"id": court.id, "location": court.location, 'accessibleDuration': court.stadium.openingHours,
                   'reservedDuration': [], 'notReservedDuration': []}
        reservedDurations = court.duration_set.all().filter(accessible=False, date=date)
        for duration in reservedDurations:
            myCourt['reservedDuration'].append((duration.id, duration.startTime, duration.endTime, duration.user.username))
        notReservedDurations = court.duration_set.all().filter(accessible=True, date=date)
        for duration in notReservedDurations:
            myCourt['notReservedDuration'].append((duration.id, duration.startTime, duration.endTime))
        myCourt["comment"] = []
        myCourts.append(myCourt)
    return JsonResponse(response)


def get_court_reserve(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Requires GET'})
    courtId = request.GET.get('courtId', '')
    durationId = request.GET.get('durationId', '')
    if not courtId or not durationId:
        return JsonResponse({'error': 'Incomplete information'})
    duration = Duration.objects.all().filter(id=int(durationId))[0]
    event = duration.reserveevent_set.all()
    return JsonResponse({'event': json(event)})


def change_duration(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    stadiumId = request.POST.get('stadiumId', '')
    managerId = request.POST.get('managerId', '')
    startDate = request.POST.get('startDate', '')
    duration = request.POST.get('duration', '')
    openTime = request.POST.get('openTime', '')
    closeTime = request.POST.get('closeTime', '')
    openHours = request.POST.get('openHours', '')
    if not stadiumId or not managerId or not startDate or not duration or not openTime or not closeTime or not openHours:
        return JsonResponse({'error': 'Incomplete information'})
    manager = Manager.objects.all().filter(id=int(managerId))[0]
    stadium = Stadium.objects.all().filter(id=int(stadiumId))[0]
    changeDuration = ChangeDuration(stadium=stadium, manager=manager, openingHours=openHours, date=startDate)
    changeDuration.save()

    # TODO: 立刻处理更改时段操作
    myStadium = stadium
    myStadium.openingHours = openHours
    myStadium.openTime = openTime
    myStadium.closeTime = closeTime
    myStadium.duration = duration
    myCourts = myStadium.court_set.all()
    myDurations = myStadium.duration_set.all()

    # 删除更改时间段后的不合法时间段，该时间段的date属性应不早于startDate
    for myDuration in myDurations:
        if judgeDate(str(myDuration.date), str(startDate)) >= 0:
            myDuration.delete()
    startDate = str(datetime.datetime.strptime(startDate, '%Y-%m-%d')).split()[0]
    foreDays = judgeDate(str(calculateDate(datetime.datetime.now().strftime('%Y-%m-%d'), myStadium.foreDays)), startDate)
    if foreDays < 0:
        return JsonResponse({'message': 'ok'})
    openHours = openHours.split()

    for openHour in openHours:
        startTime, endTime = openHour.split('-')
        totalSeconds = judgeTime(endTime, startTime)
        seconds = judgeTime(duration, "00:00")
        if totalSeconds % seconds != 0:
            return JsonResponse({'error': 'can not make durations according to temp information'})
        else:
            for k in range(int(totalSeconds // seconds)):
                endTime = (datetime.datetime.strptime(str(startTime), "%H:%M") + datetime.timedelta(seconds=seconds)).strftime('%H:%M')
                for i in range(foreDays + 1):
                    date = calculateDate(startDate, i)
                    for j in range(len(myCourts)):
                        myDuration = Duration(stadium=stadium, court=myCourts[j], startTime=startTime, endTime=endTime, date=date, openState=1, accessible=1)
                        myDuration.save()
                startTime = endTime
    return JsonResponse({'message': 'ok'})


def add_event(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    managerId = request.POST.get('managerId', '')
    courtId = request.POST.get('courtId', '')
    date = request.POST.get('date', '')
    startTime = request.POST.get('startTime', '')
    endTime = request.POST.get('endTime', '')
    if not managerId or not courtId or not date or not startTime or not endTime:
        return JsonResponse({'error': 'Incomplete information'})
    manager = Manager.objects.all().filter(id=int(managerId))[0]
    court = Court.objects.all().filter(id=int(courtId))[0]
    addEvent = AddEvent(manager=manager, court=court, startTime=startTime, endTime=endTime, date=date)
    addEvent.save()

    myDurations = court.duration_set.all().filter(date=date)
    for myDuration in myDurations:
        cp1 = judgeTime(myDuration.endTime, startTime)
        cp2 = judgeTime(startTime, myDuration.startTime)
        cp3 = judgeTime(myDuration.endTime, endTime)
        cp4 = judgeTime(endTime, myDuration.startTime)
        flag = 0
        flag += cp1 > 0 and cp2 > 0
        flag += cp3 > 0 and cp4 > 0
        flag += cp2 < 0 and cp3 < 0
        flag += cp2 > 0 and cp3 > 0
        if flag > 0:
            myDuration.openState = 0
            myDuration.save()
    return JsonResponse({'message': 'ok'})


def get_users(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Requires GET'})
    managerId = request.GET.get('managerId', '')
    if not managerId:
        return JsonResponse({'error': 'Incomplete information'})
    users = User.objects.all()
    return JsonResponse({'users': json(users)})

# def get_history(request):
#     if request.method != 'GET':
#         return JsonResponse({'error': 'Requires GET'})
#     managerId = request.GET.get('managerId', '')
#     manager = Manager.objects.all().filter(id=int(managerId))[0]
#     if not managerId:
#         return JsonResponse({'error': 'Incomplete information'})
#     changeDuration = manager.changeduration_set.all()
#     addEvent = manager.addevent_set.all()
#     return JsonResponse({'changeDuration': json(changeDuration), 'addEvent': json(addEvent)})


def get_history(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Requires GET'})
    managerId = request.GET.get('managerId', '')
    manager = Manager.objects.all().filter(id=int(managerId))[0]
    if not managerId:
        return JsonResponse({'error': 'Incomplete information'})
    changeDuration = manager.changeduration_set.all()
    addEvent = manager.addevent_set.all()
    myOperations = sorted(chain(changeDuration, addEvent), key=attrgetter('time'), reverse=True)
    operations = [model_to_dict(myOperation, fields=['time', 'type', 'id']) for myOperation in myOperations]
    return JsonResponse({'operations': operations})


"""
以下API未经过严格测试，请谨慎使用
"""


def get_detail_change(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Requires GET'})
    eventId = request.GET.get('eventId', '')
    if not eventId:
        return JsonResponse({'error': 'Incomplete information'})
    changeDuration = ChangeDuration.objects.all().filter(id=int(eventId))[0]
    return JsonResponse(model_to_dict(changeDuration))


def get_detail_event(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Requires GET'})
    eventId = request.GET.get('eventId', '')
    if not eventId:
        return JsonResponse({'error': 'Incomplete information'})
    addEvent = AddEvent.objects.all().filter(id=int(eventId))[0]
    return JsonResponse(model_to_dict(addEvent))


def revoke(request):
    return JsonResponse({'message': 'ok'})







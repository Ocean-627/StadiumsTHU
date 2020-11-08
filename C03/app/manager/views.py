from django.http import JsonResponse
from datetime import datetime
from app.models import *
import datetime
import hashlib
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


"""
以下API未经过严格测试，请谨慎使用
"""


def get_court(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Requires GET'})
    workplace = request.GET.get('workplace', '')
    floor = request.GET.get('floor', '')
    date = request.GET.get('date', '')
    if not workplace or not floor or not date:
        return JsonResponse({'error': 'Incomplete information'})
    stadium = Stadium.objects.all().filter(id=int(workplace))[0]
    courts = stadium.court_set.all()
    courts = courts.filter(floor=floor)
    response = {"floor": floor, "number": len(courts), "duration": stadium.duration}
    for court in courts:
        myCourt = {"id": court.id, "location": court.location, 'accessibleDuration': court.stadium.openingHours,
                   'reservedDuration': [], 'notReservedDuration': []}
        durations = court.duration_set.all()
        reservedDurations = durations.filter(accessible=False)
        for duration in reservedDurations:
            myCourt['reservedDuration'].append((duration.id, duration.startTime, duration.endTime, duration.user.username))
        notReservedDurations = durations.filter(accessible=False)
        for duration in notReservedDurations:
            myCourt['notReservedDuration'].append((duration.id, duration.startTime, duration.endTime))
        myCourt["comment"] = []
    return JsonResponse(response)


def get_court_reserve(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Requires GET'})
    courtId = request.GET.get('courtId', '')
    durationId = request.GET.get('durationId', '')
    if not courtId or not durationId:
        return JsonResponse({'error': 'Incomplete information'})
    event = ReserveEvent.objects.all().filter(durationId=int(durationId))[0]
    return json(event)


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
    manager = Manager.objects.all().filter(id=int(managerId))[0]
    stadium = Stadium.objects.all().filter(id=int(stadiumId))[0]
    changeDuration = ChangeDuration(stadium=stadium, manager=manager, openingHours=openHours, startDate=startDate)
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
        if judgeDate(myDuration.date, startDate) >= 0:
            myDuration.delete()

    startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    foreDays = judgeDate(calculateDate(datetime.now().strftime('%Y-%m-%d'), myStadium.foreDays), startDate)
    if foreDays < 0:
        return JsonResponse({'message': 'ok'})
    for i in range(foreDays + 1):
        date = (startDate+datetime.timedelta(days=+i)).strftime("%Y-%m-%d")
        openHours = openHours.split()
        for openHour in openHours:
            startTime, endTime = openHour.split('-')
            time_1_struct = datetime.strptime(startTime, "%H:%M")
            time_2_struct = datetime.strptime(endTime, "%H:%M")
            totalSeconds = (time_2_struct - time_1_struct).seconds / 60
            time_1_struct = datetime.strptime("00:00", "%H:%M")
            time_2_struct = datetime.strptime(duration, "%H:%M")
            seconds = (time_2_struct - time_1_struct).seconds / 60
            if totalSeconds % seconds != 0:
                return JsonResponse({'error': 'can not make durations according to temp information'})
            else:
                start = openHour.split('-')[0]
                myTime = start
                for k in range(int(totalSeconds // seconds)):
                    for j in range(len(myCourts)):
                        duration = Duration()
                        duration.name = myCourts[j].name
                        duration.startTime = myTime
                        myTime = datetime.datetime.strptime(myTime, "%H:%M") + datetime.timedelta(seconds * (i + 1))
                        duration.endTime = myTime.strftime('%H:%M')
                        duration.date = date
                        duration.save()

    return JsonResponse({'message': 'ok'})


def add_event(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    managerId = request.POST.get('managerId', '')
    courtId = request.POST.get('courtId', '')
    date = request.POST.get('date', '')
    startTime = request.POST.get('startTime', '')
    endTime = request.POST.get('endTime', '')
    manager = Manager.objects.all().filter(id=int(managerId))[0]
    court = Court.objects.all().filter(id=int(courtId))[0]
    addEvent = AddEvent(manager=manager, court=court, startTime=startTime, endTime=endTime, date=date)
    myDurations = court.duration_set.all().filter(date=date)

    for myDuration in myDurations:
        cp1 = judgeTime(myDuration.endTime, startTime)
        cp2 = judgeTime(startTime, myDuration.startTime)
        cp3 = judgeTime(myDuration.endTime, endTime)
        cp4 = judgeTime(endTime, myDuration.endTime)
        flag = 0
        flag += cp1 > 0 and cp2 > 0
        flag += cp3 > 0 and cp4 > 0
        flag += cp2 < 0 and cp3 < 0
        flag += cp2 > 0 and cp3 > 0
        if flag > 0:
            myDuration.openState = 2
    addEvent.save()



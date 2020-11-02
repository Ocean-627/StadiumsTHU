from django.http import JsonResponse
from datetime import datetime
from app.models import *
import datetime
import hashlib


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
    courts = Court.objects.all()
    courts = courts.filter(stadiumId=workplace)
    # TODO: 根据楼层筛选
    # courts = courts.filter(floor=floor)
    response = {}
    response["floor"] = floor
    response["number"] = len(courts)
    response["duration"] = stadium.duration
    returnCourts = []
    durations = Duration.objects.all()
    for item in courts:
        myCourt = {}
        myCourt["id"] = item.id
        myCourt["location"] = ""
        myCourt['accessibleDuration'] = []
        openHours = item.openingHours.split()
        for openHour in openHours:
            time = openHour.split('-')
            myCourt['accessibleDuration'].append((time[0], time[1]))
        reservedDurations = durations.filter(courtId=item.id, accessible=False)
        myCourt['reservedDuration'] = []

        # TODO: duration中添加预订者及预订者学号等信息
        for duration in reservedDurations:
            myCourt['reservedDuration'].append((duration.id, duration.startTime, duration.endTime))

        notReservedDurations = durations.filter(courtId=item.id, accessible=False)
        myCourt['notReservedDuration'] = []
        # TODO: duration中添加预订者及预订者学号等信息
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
    court = Court.objects.all().filter(id=int(courtId))[0]
    duration = Duration.objects.all().filter(id=int(durationId))[0]
    # TODO: ReserveEvent中添加预订时期Id
    event = ReserveEvent.objects.all().filter(durationId=int(durationId))[0]
    response = {}
    response["userId"] = event.userId
    response["eventId"] = event.id
    response["startTime"] = event.startTime
    response["endTime"] = event.endTime
    response["cancle"] = event.cancle
    response["payment"] = event.checked
    response["checked"] = event.checked
    response["repayment"] = event.repayment
    response["leave"] = event.leave
    return JsonResponse(response)


def change_duration(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires GET'})
    stadiumId = request.POST.get('id', '')
    username = request.POST.get('username', '')
    stadium = request.POST.get('stadium', '')
    startDate = request.POST.get('startDate', '')
    duration = request.POST.get('duration', '')
    openTime = request.POST.get('openTime', '')
    closeTime = request.POST.get('closeTime', '')
    openHours = request.POST.get('openHours', '')
    changeDuration = ChangeDuration(stadiumId=stadiumId, openingHours=openHours, startDate=startDate)
    changeDuration.save()

    # TODO: 立刻处理更改时段操作
    myStadium = Stadium.objects.all().filter(id=stadiumId)[0]
    myStadium.openingHours = openHours
    myStadium.openTime = openTime
    myStadium.closeTime = closeTime
    myStadium.duration = duration
    myCourts = Court.objects.all().filter(stadiumId=stadiumId)
    for myCourt in myCourts:
        myCourt.openingHours = openHours
    myDurations = Duration.objects.all().filter(stadiumId=stadiumId)
    for myDuration in myDurations:
        target_time = myDuration.date
        cur_time = datetime.now()
        format_pattern = '%Y-%m-%d'
        cur_time = cur_time.strftime(format_pattern)
        difference = (datetime.strptime(target_time, format_pattern) - datetime.strptime(cur_time, format_pattern))
        if difference.days >= 0:
            myDuration.delete()
    target_time = startDate
    cur_time = datetime.now()
    format_pattern = '%Y-%m-%d'
    cur_time = cur_time.strftime(format_pattern)
    difference = (datetime.strptime(target_time, format_pattern) - datetime.strptime(cur_time, format_pattern))
    if difference.days <= myStadium:
        return JsonResponse({'message': 'ok'})
    else:
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
                end = openHour.split('-')[1]
                myTime = start
                for i in range(int(totalSeconds//seconds)):
                    for j in range(len(myCourts)):
                        # TODO: 添加时段并完善相关信息操作
                        duration = Duration()
                        duration.name = myCourts[j].name
                        duration.startTime = myTime
                        myTime = datetime.datetime.strptime(myTime, "%H:%M") + datetime.timedelta(seconds)
                        duration.endTime = myTime.strftime('%H:%M')
                        duration.save()

    return JsonResponse({'message': 'ok'})


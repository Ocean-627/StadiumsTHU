from django.http import JsonResponse
from itertools import chain
from operator import attrgetter
from app.utils.utils import *
from app.utils.serializer import *
from app.utils.authtication import ManagerAuthtication
from rest_framework.views import APIView
from rest_framework.response import Response


class LogonView(APIView):
    """
    管理员注册
    """

    def post(self, request):
        req_data = request.data
        username = req_data.get('username')
        password = req_data.get('password')
        email = req_data.get('email')
        userId = req_data.get('userId')
        stadiumId = req_data.get('stadiumId')
        # TODO:检查stadium是否存在
        if not username or not password or not email or not userId or not stadiumId:
            return Response({'error': 'Incomplete information'})
        manager = Manager(username=username, password=password, email=email, userId=userId, stadium_id=stadiumId)
        manager.save()
        return Response({'message': 'ok'})


class LoginView(APIView):
    """
    管理员登录
    """

    def post(self, request):
        req_data = request.data
        userId = req_data.get('userId')
        password = req_data.get('password')
        obj = Manager.objects.filter(userId=userId, password=password).first()
        if not obj:
            return Response({'error': 'Login failed'})
        loginToken = md5(userId)
        obj.loginToken = loginToken
        print(loginToken)
        obj.save()
        ret = Response(
            {'message': 'ok', 'username': obj.username, 'stadium': obj.stadium.name,
             'stadiumId': obj.stadium.id})
        ret.set_cookie('loginToken', loginToken)
        return ret


class LogoutView(APIView):
    """
    管理员注销
    """
    authentication_classes = [ManagerAuthtication]

    def post(self, request):
        manager = request.user
        manager.loginToken = ''
        manager.save()
        ret = JsonResponse({'message': 'ok'})
        ret.delete_cookie('loginToken')
        return ret


class StadiumView(APIView):
    """
    场馆信息
    """

    # authentication_classes = [ManagerAuthtication]
    def get(self, request):
        myStadium = Stadium.objects.all()
        stadiums = json(myStadium)
        for i in range(len(stadiums)):
            stadiums[i]["courtTypes"] = []
            for courtType in list(myStadium[i].courttype_set.all()):
                stadiums[i]["courtTypes"].append({"name": courtType.type,
                                                  "openHours": courtType.openingHours,
                                                  "amount": len(courtType.court_set.all())})
        return JsonResponse({"stadiums": stadiums})


class CourtView(APIView):
    """
    场地信息
    """
    authentication_classes = [ManagerAuthtication]

    def get(self, request):
        req_data = request.query_params
        workplace = req_data.get('stadiumId', '')
        floor = req_data.get('floor', '')
        date = req_data.get('date', '')
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
                myCourt['reservedDuration'].append(
                    (duration.id, duration.startTime, duration.endTime, duration.user.username))
            notReservedDurations = court.duration_set.all().filter(accessible=True, date=date)
            for duration in notReservedDurations:
                myCourt['notReservedDuration'].append((duration.id, duration.startTime, duration.endTime))
            myCourt["comment"] = []
            myCourts.append(myCourt)
        return JsonResponse(response)


class ReserveEventView(APIView):
    """
    预约信息
    """
    authentication_classes = [ManagerAuthtication]

    def get(self, request):
        req_data = request.query_params
        courtId = req_data.get('courtId', '')
        durationId = req_data.get('durationId', '')
        if not courtId or not durationId:
            return JsonResponse({'error': 'Incomplete information'})
        duration = Duration.objects.all().filter(id=int(durationId))[0]
        event = duration.reserveevent_set.all()
        return JsonResponse({'event': json(event)})


class ChangeDurationView(APIView):
    """
    修改预约时段信息
    """

    # authentication_classes = [ManagerAuthtication]

    def post(self, request):
        req_data = request.data
        stadiumId = req_data.get('stadiumId', '')
        print(request)
        managerId = req_data.get('managerId', '')
        startDate = req_data.get('startDate', '')
        duration = req_data.get('duration', '')
        openTime = req_data.get('openTime', '')
        closeTime = req_data.get('closeTime', '')
        openHours = req_data.get('openHours', '')
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
        foreDays = judgeDate(str(calculateDate(datetime.datetime.now().strftime('%Y-%m-%d'), myStadium.foreDays)),
                             startDate)
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
                    endTime = (datetime.datetime.strptime(str(startTime), "%H:%M") + datetime.timedelta(
                        seconds=seconds)).strftime('%H:%M')
                    for i in range(foreDays + 1):
                        date = calculateDate(startDate, i)
                        for j in range(len(myCourts)):
                            myDuration = Duration(stadium=stadium, court=myCourts[j], startTime=startTime,
                                                  endTime=endTime, date=date, openState=1, accessible=1)
                            myDuration.save()
                    startTime = endTime
        return JsonResponse({'message': 'ok'})

    def get(self, request):
        req_data = request.query_params
        eventId = req_data.get('eventId', '')
        if not eventId:
            return JsonResponse({'error': 'Incomplete information'})
        changeDuration = ChangeDuration.objects.all().filter(id=int(eventId))[0]
        return JsonResponse(model_to_dict(changeDuration))


class AddEventView(APIView):
    """
    添加场地占用事件信息
    """
    authentication_classes = [ManagerAuthtication]

    def post(self, request):
        req_data = request.data
        managerId = req_data.get('managerId', '')
        courtId = req_data.get('courtId', '')
        date = req_data.get('date', '')
        startTime = req_data.get('startTime', '')
        endTime = req_data.get('endTime', '')
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

    def get(self, request):
        req_data = request.query_params
        eventId = req_data.get('eventId', '')
        if not eventId:
            return JsonResponse({'error': 'Incomplete information'})
        addEvent = AddEvent.objects.all().filter(id=int(eventId))[0]
        return JsonResponse(model_to_dict(addEvent))


class UsersView(APIView):
    """
    用户信息
    """
    authentication_classes = [ManagerAuthtication]

    def get(self, request):
        req_data = request.query_params
        managerId = req_data.get('managerId', '')
        if not managerId:
            return JsonResponse({'error': 'Incomplete information'})
        users = User.objects.all()
        return JsonResponse({'users': json(users)})


class HistoryView(APIView):
    """
    历史操作信息
    """
    authentication_classes = [ManagerAuthtication]

    def get(self, request):
        req_data = request.query_params
        managerId = req_data.get('managerId', '')
        manager = Manager.objects.all().filter(id=int(managerId))[0]
        if not managerId:
            return JsonResponse({'error': 'Incomplete information'})
        changeDuration = manager.changeduration_set.all()
        addEvent = manager.addevent_set.all()
        myOperations = sorted(chain(changeDuration, addEvent), key=attrgetter('time'), reverse=True)
        operations = [model_to_dict(myOperation, fields=['time', 'type', 'id']) for myOperation in myOperations]
        return JsonResponse({'operations': operations})

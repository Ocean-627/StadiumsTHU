from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.utils.timezone import now
import datetime
import pytz
import time
from app.models import *
from app.utils.utils import *


class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(label='用户昵称', validators=[MinLengthValidator(3), MaxLengthValidator(20)],
                                     required=False)
    phone = serializers.CharField(label='手机号', validators=[MinLengthValidator(11), MaxLengthValidator(11)],
                                  required=False)

    class Meta:
        model = User
        fields = '__all__'
        # 设置read_only起到了保护的作用，即用户不能修改这些字段
        read_only_fields = ['loginToken', 'loginTime', 'userId', 'defaults', 'blacklist']


class StadiumSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(required=False)
    comments = serializers.SerializerMethodField(required=False)
    score = serializers.SerializerMethodField(required=False)
    collect = serializers.SerializerMethodField(required=False)
    courtTypes = serializers.SerializerMethodField(required=False)

    def get_images(self, obj):
        images_list = obj.stadiumimage_set.all()
        images_list = StadiumImageSerializer(images_list, many=True)
        return images_list.data

    def get_courtTypes(self, obj):
        types = obj.courttype_set.all()
        types = CourtTypeSerializer(types, many=True)
        return types.data

    def get_comments(self, obj):
        court_list = obj.court_set.all()
        tot = 0
        for court in court_list:
            tot += len(court.comment_set.all())
        return tot

    def get_score(self, obj):
        court_list = obj.court_set.all()
        tot_score = 0
        tot_num = 0
        for court in court_list:
            tot_num += len(court.comment_set.all())
            for comment in court.comment_set.all():
                tot_score += comment.score
        if tot_num == 0:
            return 3
        else:
            return tot_score / tot_num

    def get_collect(self, obj):
        res = obj.collectevent_set.filter(user=self.context['request'].user).first()
        if not res:
            return None
        return res.id

    class Meta:
        model = Stadium
        exclude = ['information', 'contact', 'foreDays']


class StadiumDetailSerializer(StadiumSerializer):
    class Meta:
        model = Stadium
        fields = '__all__'


class CourtTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtType
        exclude = ['stadium']


class CourtSerializer(serializers.ModelSerializer):
    stadiumName = serializers.CharField(source='stadium.name')
    foreDays = serializers.IntegerField(source='stadium.foreDays')

    class Meta:
        model = Court
        fields = '__all__'


class DurationSerializer(serializers.ModelSerializer):
    stadiumName = serializers.CharField(source='stadium.name')
    courtName = serializers.CharField(source='court.name')

    class Meta:
        model = Duration
        fields = '__all__'


class ReserveEventSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField(required=False)
    image = serializers.SerializerMethodField(required=False)
    price = serializers.SerializerMethodField(required=False)
    type = serializers.SerializerMethodField(required=False)

    def get_result(self, obj):
        return obj.get_result_display()

    def get_comments(self, obj):
        comments = Comment.objects.filter(reserve_id=obj.id)
        comments = CommentSerializer(comments, many=True)
        return comments.data

    def get_image(self, obj):
        stadium = Stadium.objects.get(id=obj.stadium_id)
        image = stadium.stadiumimage_set.first()
        if not image:
            return None
        return image.image.url

    def get_price(self, obj):
        court = Court.objects.get(id=obj.court_id)
        price = court.courtType.price
        return price

    def get_type(self, obj):
        court = Court.objects.get(id=obj.court_id)
        type = court.courtType.type
        return type

    duration_id = serializers.IntegerField(label='时段编号')

    def validate_duration_id(self, value):
        duration = Duration.objects.filter(id=value, accessible=True).first()
        if not duration:
            raise ValidationError('Invalid duration_id')
        myDate = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
        myTime = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%H:%M')
        if judgeTime(duration.startTime, myTime) < 0 and duration.date == myDate:
            raise ValidationError('Invalid duration_id, you should not reserve duration that passed')
        return value

    def create(self, validated_data):
        duration = Duration.objects.filter(id=validated_data.get('duration_id')).first()
        stadium = duration.stadium
        court = duration.court
        # modify corresponding duration
        duration.accessible = False
        duration.user = self.context['request'].user
        duration.save()
        # send reserve success message
        content = '您已经成功预约' + stadium.name + court.name + '预约时间为' + duration.date + ',' + duration.startTime + '-' + duration.endTime + '。'
        News.objects.create(user=self.context['request'].user, type='预约成功', content=content)
        return ReserveEvent.objects.create(user=self.context['request'].user, **validated_data, stadium=stadium.name,
                                           stadium_id=stadium.id, court=court.name, date=duration.date,
                                           court_id=court.id,
                                           startTime=duration.startTime, endTime=duration.endTime,
                                           result='S')

    class Meta:
        model = ReserveEvent
        fields = '__all__'
        read_only_fields = ['user', 'stadium', 'court', 'stadium_id', 'court_id', 'date', 'result', 'startTime',
                            'endTime', 'has_comments']


class ReserveModifySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    def validate_event_id(self, value):
        reserve = ReserveEvent.objects.filter(user=self.context['request'].user, id=value).first()
        if not reserve:
            raise ValidationError('Invalid id')
        return value

    class Meta:
        model = ReserveEvent
        fields = ['id', 'payment', 'cancel', 'checked', 'leave']


class CommentSerializer(serializers.ModelSerializer):
    courtName = serializers.CharField(source='court.name', required=False)
    images = serializers.SerializerMethodField(required=False)

    reserve_id = serializers.IntegerField(label='预订编号', write_only=True)
    content = serializers.CharField(label='评论内容', validators=[MinLengthValidator(5), MaxLengthValidator(300)])

    def get_images(self, obj):
        images_list = obj.commentimage_set.all()
        images_list = CommentImageSerializer(images_list, many=True)
        return images_list.data

    def validate_reserve_id(self, value):
        event = ReserveEvent.objects.filter(id=value, user=self.context['request'].user).first()
        if not event:
            raise ValidationError('Invalid reserve_id')
        return value

    def create(self, validated_data):
        event = ReserveEvent.objects.filter(id=validated_data.get('reserve_id')).first()
        event.has_comments = True
        event.save()
        court = Court.objects.get(id=event.court_id)
        stadium_id = court.stadium.id
        comment = Comment.objects.create(user=event.user, court=court, stadium_id=stadium_id, **validated_data)
        return comment

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'court', 'stadium_id']


class CommentImageSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(label='评论编号', write_only=True)

    def validate_comment_id(self, value):
        comment = Comment.objects.filter(id=value, user=self.context['request'].user).first()
        if not comment:
            raise ValidationError('Invalid comment_id')
        return value

    class Meta:
        model = CommentImage
        fields = '__all__'
        read_only_fields = ['comment']


class StadiumImageSerializer(serializers.ModelSerializer):
    stadium_id = serializers.IntegerField(label='场馆编号', write_only=True)

    def validate_stadium_id(self, value):
        stadium = Stadium.objects.filter(id=value).first()
        if not stadium:
            raise ValidationError('Invalid stadium_id')
        return value

    class Meta:
        model = StadiumImage
        fields = '__all__'
        read_only_fields = ['stadium']


class CollectEventSerializer(serializers.ModelSerializer):
    stadium_name = serializers.CharField(source='stadium.name', required=False)
    stadium_id = serializers.IntegerField(label='场馆编号', write_only=True)

    def validate_stadium_id(self, value):
        stadium = Stadium.objects.filter(id=value).first()
        if not stadium:
            raise ValidationError('Invalid stadium_id')
        collect = stadium.collectevent_set.filter(user=self.context['request'].user).first()
        if collect:
            raise ValidationError('You have collect that stadium')
        return value

    def create(self, validated_data):
        return CollectEvent.objects.create(user=self.context['request'].user, **validated_data)

    class Meta:
        model = CollectEvent
        fields = '__all__'
        read_only_fields = ['stadium', 'user']


class SessionSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField(required=False)

    def get_messages(self, obj):
        message_list = obj.message_set.all()
        message_list = MessageSerializer(message_list, many=True)
        return message_list.data

    def create(self, validated_data):
        user = self.context['request'].user
        return Session.objects.create(user_id=user.id, **validated_data)

    class Meta:
        model = Session
        fields = '__all__'
        read_only_fields = ['user_id']


class MessageSerializer(serializers.ModelSerializer):
    session_id = serializers.IntegerField(label='会话编号', write_only=True)

    def validate_session_id(self, value):
        user = self.context['request'].user
        session = Session.objects.filter(id=value, user_id=user.id).first()
        if not session:
            raise ValidationError('Invalid session_id')
        return value

    def create(self, validated_data):
        message = Message.objects.create(sender='U', **validated_data)
        session = message.session
        session.checked = False
        session.save()
        return message

    class Meta:
        model = Message
        exclude = ['manager_id']
        read_only_fields = ['session', 'sender']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['createTime', 'type', 'user', 'content']


class DefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Default
        fields = '__all__'
        read_only_fields = ['user']

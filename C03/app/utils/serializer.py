from rest_framework import serializers
from rest_framework.serializers import ValidationError

from app.models import *


class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(label='用户昵称', validators=[MinLengthValidator(3), MaxLengthValidator(20)],
                                     required=False)
    phone = serializers.CharField(label='手机号', validators=[MinLengthValidator(11), MaxLengthValidator(11)],
                                  required=False)
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        images_list = obj.userimage_set.all()
        images_list = UserImageSerializer(images_list, many=True)
        return images_list.data

    class Meta:
        model = User
        fields = '__all__'
        # 设置read_only起到了保护的作用，即用户不能修改这些字段
        read_only_fields = ['openId', 'loginToken', 'loginTime']


class StadiumSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(required=False)
    comments = serializers.SerializerMethodField(required=False)
    score = serializers.SerializerMethodField(required=False)
    courtTypes = serializers.SerializerMethodField(required=False)

    def get_images(self, obj):
        images_list = obj.stadiumimage_set.all()
        images_list = StadiumImageSerializer(images_list, many=True)
        return images_list.data

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

    def get_courtTypes(self, obj):
        types = obj.courttype_set.all()
        types = CourtTypeSerializer(types, many=True)
        return types.data

    class Meta:
        model = Stadium
        fields = '__all__'


class CourtTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtType
        exclude = ['id', 'stadium']


class CourtSerializer(serializers.ModelSerializer):
    stadiumName = serializers.CharField(source='stadium.name')

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
    stadiumName = serializers.CharField(source='stadium.name', required=False)
    courtName = serializers.CharField(source='court.name', required=False)
    userName = serializers.CharField(source='user.username', required=False)

    duration_id = serializers.IntegerField(label='时段编号', write_only=True)

    result = serializers.SerializerMethodField()

    def validate_duration_id(self, value):
        duration = Duration.objects.filter(id=value, accessible=True).first()
        if not duration:
            raise ValidationError('Invalid duration_id')
        return value

    def get_result(self, obj):
        return obj.get_result_display()

    def create(self, validated_data):
        duration = Duration.objects.filter(id=validated_data.get('duration_id')).first()
        stadium = duration.stadium
        court = duration.court
        # modify corresponding duration
        duration.accessible = False
        duration.user = self.context['request'].user
        duration.save()
        return ReserveEvent.objects.create(user=self.context['request'].user, **validated_data, stadium=stadium,
                                           court=court, startTime=duration.startTime, endTime=duration.endTime,
                                           result='S')

    class Meta:
        model = ReserveEvent
        fields = '__all__'
        read_only_fields = ['user', 'stadium', 'court', 'duration', ' result', 'startTime', 'endTime']


class CommentSerializer(serializers.ModelSerializer):
    courtName = serializers.CharField(source='court.name', required=False)
    images = serializers.SerializerMethodField(required=False)

    court_id = serializers.IntegerField(label='场馆编号', write_only=True)
    content = serializers.CharField(label='评论内容', validators=[MinLengthValidator(15), MaxLengthValidator(300)])

    def get_images(self, obj):
        images_list = obj.commentimage_set.all()
        images_list = CommentImageSerializer(images_list, many=True)
        return images_list.data

    def validate_court_id(self, value):
        court = Court.objects.filter(id=value).first()
        if not court:
            raise ValidationError('Invalid court_id')
        return value

    def create(self, validated_data):
        comment = Comment.objects.create(user=self.context['request'].user, **validated_data)
        return comment

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'court']


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
    class Meta:
        model = StadiumImage
        fields = '__all__'


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = '__all__'

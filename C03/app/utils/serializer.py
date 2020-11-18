from rest_framework import serializers
from app.models import *


class UserSerializer(serializers.ModelSerializer):
    # 用来验证用户输入
    username = serializers.CharField(label='用户名', validators=[MinLengthValidator(3), MaxLengthValidator(32)])
    password = serializers.CharField(label='密码',
                                     validators=[MinLengthValidator(10), MaxLengthValidator(32), SafeValidator])

    class Meta:
        model = User
        fields = '__all__'


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = '__all__'


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
    stadiumName = serializers.CharField(source='stadium.name')
    courtName = serializers.CharField(source='court.name')
    userName = serializers.CharField(source='user.username')
    result = serializers.SerializerMethodField()

    def get_result(self, obj):
        return obj.get_result_display()

    class Meta:
        model = ReserveEvent
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    courtName = serializers.CharField(source='court.name', required=False)
    images = serializers.SerializerMethodField(required=False)
    content = serializers.CharField(label='评论内容', validators=[MinLengthValidator(15), MaxLengthValidator(300)])

    def get_images(self, obj):
        images_list = obj.commentimage_set.all()
        images_list = CommentImageSerializer(images_list, many=True)
        return images_list.data

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['court', 'user']


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = '__all__'

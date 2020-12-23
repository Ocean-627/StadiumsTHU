from app.utils.user_serializer import *
from app.utils.validator import *


class ChangeDurationSerializer(serializers.ModelSerializer):
    courtType_id = serializers.IntegerField(label='场馆类型编号', write_only=True)
    state = serializers.SerializerMethodField()

    def get_state(self, obj):
        return obj.get_state_display()

    def validate_courtType_id(self, value):
        courtType = CourtType.objects.filter(id=value).first()
        if not courtType:
            raise ValidationError('Invalid courtType_id')
        return value

    def create(self, validated_data):
        manager = self.context['request'].user
        content = '管理员' + manager.username + '修改了预约时间段'
        return ChangeDuration.objects.create(manager=manager, content=content, **validated_data)

    class Meta:
        model = ChangeDuration
        fields = '__all__'
        read_only_fields = ['manager', 'courtType', 'content']


class AddEventSerializer(serializers.ModelSerializer):
    court_id = serializers.IntegerField(label='场地编号', write_only=True)
    state = serializers.SerializerMethodField()

    def get_state(self, obj):
        return obj.get_state_display()

    def validate_court_id(self, value):
        court = Court.objects.filter(id=value).first()
        if not court:
            raise ValidationError('Invalid court_id')
        return value

    def create(self, validated_data):
        manager = self.context['request'].user
        court = Court.objects.filter(id=validated_data.get('court_id')).first()
        content = '管理员' + manager.username + '占用了' + court.stadium + court.name
        return AddEvent.objects.create(content=content, **validated_data)

    class Meta:
        model = AddEvent
        fields = '__all__'
        read_only_fields = ['manager', 'court', 'state', 'content']


class AddBlacklistSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(label='用户编号', write_only=True)
    state = serializers.SerializerMethodField()

    def get_state(self, obj):
        return obj.get_state_display()

    def validate_user_id(self, value):
        user = User.objects.filter(id=value, inBlacklist=False).first()
        if not user:
            raise ValidationError('Invalid user_id')
        return value

    def create(self, validated_data):
        user = User.objects.get(id=validated_data.get('user_id'))
        user.inBlacklist = True
        user.inBlacklistTime = timezone.now().date()
        user.save()
        manager = self.context['request'].user
        content = '管理员' + manager.username + '将' + user.name + '加入黑名单'
        return AddBlacklist.objects.create(manager=self.context['request'].user, content=content, **validated_data)

    class Meta:
        model = AddBlacklist
        fields = '__all__'
        read_only_fields = ['manager', 'user', 'content']


class HistorySerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1, validators=[MinValueValidator(1)])
    size = serializers.IntegerField(default=15, validators=[MinValueValidator(1)])


class OperationSerailizer(serializers.Serializer):
    time = serializers.DateTimeField()
    type = serializers.CharField()
    id = serializers.IntegerField()
    state = serializers.IntegerField()
    details = serializers.CharField()
    content = serializers.CharField()


class NumberSerializer(serializers.Serializer):
    num = serializers.IntegerField(validators=[MinValueValidator(1)])

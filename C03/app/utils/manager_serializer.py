from app.utils.serializer import *


class StadiumSerializerForManager(StadiumSerializer):
    stadium_id = serializers.IntegerField(write_only=True)
    courtTypes = serializers.SerializerMethodField(required=False)

    def validate_stadium_id(self, value):
        stadium = Stadium.objects.filter(id=value).first()
        if not stadium:
            raise ValidationError('Invalid stadium_id')
        return value

    def get_courtTypes(self, obj):
        types = obj.courttype_set.all()
        types = CourtTypeSerializerForManager(types, many=True)
        return types.data

    def get_collect(self, obj):
        return None

    class Meta:
        model = Stadium
        fields = '__all__'
        read_only_fields = ['openTime', 'closeTime', 'foreDays', 'openState']


class CourtTypeSerializerForManager(CourtTypeSerializer):
    amount = serializers.SerializerMethodField(required=False)

    def get_amount(self, obj):
        return len(obj.court_set.all())


class ChangeScheduleSerializer(serializers.ModelSerializer):
    stadium_id = serializers.IntegerField(label='场馆编号', write_only=True)

    def validate_stadium_id(self, value):
        stadium = Stadium.objects.filter(id=value).first()
        if not stadium:
            raise ValidationError('Invalid stadium_id')
        return value

    def create(self, validated_data):
        return ChangeSchedule.objects.create(manager=self.context['request'].user, **validated_data)

    class Meta:
        model = ChangeSchedule
        fields = '__all__'
        read_only_fields = ['manager', 'stadium']


class ChangeDurationSerializer(serializers.ModelSerializer):
    courtType_id = serializers.IntegerField(label='场馆类型编号', write_only=True)

    def validate_courtType_id(self, value):
        courtType = CourtType.objects.filter(id=value).first()
        if not courtType:
            raise ValidationError('Invalid courtType_id')
        return value

    def create(self, validated_data):
        return ChangeDuration(manager=self.context['request'].user, **validated_data)

    class Meta:
        model = ChangeDuration
        fields = '__all__'
        read_only_fields = ['manager', 'courtType']


class AddEventSerializer(serializers.ModelSerializer):
    court_id = serializers.IntegerField(label='场地编号', write_only=True)

    def validate_court_id(self, value):
        court = Court.objects.filter(id=value).first()
        if not court:
            raise ValidationError('Invalid court_id')
        return value

    def create(self, validated_data):
        return AddEvent.objects.create(manager=self.context['request'].user, **validated_data)

    class Meta:
        model = AddEvent
        fields = '__all__'
        read_only_fields = ['manager', 'court']

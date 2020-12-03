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

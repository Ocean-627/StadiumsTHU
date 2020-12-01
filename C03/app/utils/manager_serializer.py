from app.utils.serializer import *


class StadiumSerializerForManager(StadiumSerializer):
    courtTypes = serializers.SerializerMethodField(required=False)

    def get_courtTypes(self, obj):
        types = obj.courttype_set.all()
        types = CourtTypeSerializerForManager(types, many=True)
        return types.data

    def get_collect(self, obj):
        return None


class CourtTypeSerializerForManager(CourtTypeSerializer):
    amount = serializers.SerializerMethodField(required=False)

    def get_amount(self, obj):
        return len(obj.court_set.all())

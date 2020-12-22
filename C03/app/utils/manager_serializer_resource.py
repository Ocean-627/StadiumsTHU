from app.utils.user_serializer import *
from app.utils.validator import *


class LogonSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='用户名', validators=[MinLengthValidator(3), MaxLengthValidator(20)])
    password = serializers.CharField(label='密码',
                                     validators=[MinLengthValidator(8), MaxLengthValidator(18), SafeValidator])

    class Meta:
        model = Manager
        fields = '__all__'


class ManagerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='用户名', validators=[MinLengthValidator(3), MaxLengthValidator(20)],
                                     required=False)
    password = serializers.CharField(label='密码',
                                     validators=[MinLengthValidator(8), MaxLengthValidator(18), SafeValidator],
                                     required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Manager
        fields = '__all__'
        read_only_fields = ['userId', 'loginToken']


class StadiumSerializerForManager(StadiumSerializer):
    stadium_id = serializers.IntegerField(write_only=True)
    courtTypes = serializers.SerializerMethodField(required=False)
    name = serializers.CharField(validators=[MaxLengthValidator(32)], required=False)
    information = serializers.CharField(validators=[MaxLengthValidator(300)], required=False)

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
        read_only_fields = ['openTime', 'closeTime', 'foreDays', 'openState', 'createTime']


class CreateStadiumSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Stadium.objects.create(openState=0, **validated_data)

    class Meta:
        model = Stadium
        fields = '__all__'
        read_only_fields = ['openState']


class CourtTypeSerializerForManager(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField(required=False)
    stadium_id = serializers.IntegerField(write_only=True)

    def validate_stadium_id(self, value):
        stadium = Stadium.objects.filter(id=value).first()
        if not stadium:
            raise ValidationError('Invalid stadium_id')
        return value

    def get_amount(self, obj):
        return len(obj.court_set.all())

    def create(self, validated_data):
        return CourtType.objects.create(openState=0, **validated_data)

    class Meta:
        model = CourtType
        fields = '__all__'
        read_only_fields = ['openState', 'stadium']


class ReserveEventSerializerForManager(ReserveEventSerializer):
    userName = serializers.SerializerMethodField(required=False)

    def get_userName(self, obj):
        return obj.user.name


class CommentSerializerForManager(CommentSerializer):
    stadiumName = serializers.SerializerMethodField(required=False)
    userName = serializers.SerializerMethodField(required=False)

    def get_userName(self, obj):
        return obj.user.name

    def get_stadiumName(self, obj):
        return obj.court.stadium.name


class SessionSerializerForManager(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)
    userName = serializers.SerializerMethodField(required=False)
    messages = serializers.SerializerMethodField(required=False)

    def validate_user_id(self, value):
        user = User.objects.filter(id=value).first()
        if not user:
            raise ValidationError('Invalid user_id')
        return value

    def get_image(self, obj):
        user = User.objects.get(id=obj.user_id)
        if not user.image:
            return None
        return user.image.url

    def get_userName(self, obj):
        user = User.objects.get(id=obj.user_id)
        return user.name

    def get_messages(self, obj):
        message_list = obj.message_set.all()
        message_list = MessageSerializer(message_list, many=True)
        return message_list.data

    def create(self, validated_data):
        return Session.objects.create(**validated_data)

    class Meta:
        model = Session
        fields = '__all__'


class MessageSerializerForManager(serializers.ModelSerializer):
    session_id = serializers.IntegerField(label='会话编号', write_only=True)

    def validate_session_id(self, value):
        session = Session.objects.filter(id=value).first()
        if not session:
            raise ValidationError('Invalid session_id')
        return value

    def create(self, validated_data):
        manager = self.context['request'].user
        message = Message.objects.create(sender='M', manager_id=manager.id, **validated_data)
        session = message.session
        session.checked = True
        session.save()
        return message

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['session', 'sender', 'manager_id']


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.models import Q
from accounts.api.utils import jwt_response_payload_handler
from rest_framework_jwt.settings import api_settings
from rest_framework.reverse import reverse as api_reverse
import datetime
from django.conf import settings
from django.utils import timezone
from status.serializers import SingleUserSerializer


expiare_delta = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

User = get_user_model()


class UserStatusSerializer(serializers.ModelSerializer):

    status_list = serializers.SerializerMethodField(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id','username','uri','status_list']
        
    def get_uri(self,obj):
        request = self.context.get('request')

        return api_reverse("api-user:detail",kwargs={'username':obj.username},request=request)
        #return "api/users/{user}".format(user=obj.username)

    def get_status_list(self,obj):

        request = self.context.get('request')

        limit = 2

        if request:

            limit_query = request.GET.get('limit')
            try:
                limit = int(limit_query)
            except:
                pass

        qs = obj.status_set.all().order_by("-timestamp")

        data = {
            'uri':self.get_uri(obj),
            'last':SingleUserSerializer(qs.first()).data,
            'recent':SingleUserSerializer(qs[:limit],many=True).data
        }
        return data


class userSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    token_response = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = User
        fields = ['username','email','password','confirm_password','token','expires','token_response']

        extra_kwargs = {'passwrod':{'write_only':True}}

    def get_token_response(self,obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        response = jwt_response_payload_handler(token,user,request=None)

        return response

    def get_expires(self,obj):

        contetx = self.context
        request = contetx['request']
        print(request.user.is_authenticated)

        return timezone.now() + expiare_delta - datetime.timedelta(seconds=200)

    def get_token(self,obj):

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)

        return token

    def validate_username(self,value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('This username already taken')
        return value

    def validate_email(sefl,value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('This email already taken')
        return value


    def validate(self,data):

        pw = data.get('password')
        pw2 = data.get('confirm_password')

        if pw != pw2 :

            raise serializers.ValidationError('Password not matche!')

        return data

    def create(self,validate_data):

        username = validate_data.get('username')
        email = validate_data.get('email')
        password = validate_data.get('password')

        user = User(username=username,email=email)

        user.set_password(password)

        user.save()

        return user



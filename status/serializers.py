from rest_framework import serializers
from .models import Status
from django.contrib.auth import get_user_model
User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id','username','uri']
        
    def get_uri(self,obj):
        return "http://127.0.0.1:8000/api/user/{user}".format(user=obj.username)



class statusSerializer(serializers.ModelSerializer):

    user = UserDetailSerializer(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Status
        fields = ['id','user','content','slug','image','uri']
        read_only_fields = ['user','slug']                   

    def get_uri(self,obj):

        return "http://127.0.0.1:8000/api/status/{id}".format(id=obj.id)

    def validate_content(self,value):

        if len(value) > 240:
            raise serializers.ValidationError('Content is too long')
        return value

class SingleUserSerializer(serializers.ModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Status
        fields = ['id','content','slug','image','uri']
        read_only_fields = ['slug']                   

    def get_uri(self,obj):

        return "http://127.0.0.1:8000/api/status/{id}".format(id=obj.id)

    def get_image(self,obj):

        if obj.image == "":

            return ""

        else:
            
            return "http://127.0.0.1:8000/media/{image}".format(image=obj.image)

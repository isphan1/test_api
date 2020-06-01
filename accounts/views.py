from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics,permissions,pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, get_user_model
from accounts.api.utils import jwt_response_payload_handler
from accounts.api.userSerializer import userSerializer
from accounts.api.userSerializer import UserStatusSerializer
from rest_framework_jwt.settings import api_settings
from accounts.api.permissions import UserPermission

jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

# Create your views here.

User = get_user_model()

class AuthApiView(APIView):

    permission_classes = [UserPermission]

    def post(self,request,*args,**kwargs):

        if request.user.is_authenticated:
            return Response({'detail':'You are already authenticated.'},status=400)

        data = request.data

        username  = data.get('username')
        password  = data.get('password')

        user = authenticate(username=username,password=password)

        qs = User.objects.filter(
            Q(username__iexact=username)|
            Q(email__iexact=username)
        ).distinct()

        if qs.count() == 1:
            user_obj = qs.first()

            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token,user,request=request)

                return Response(response)

        return Response({'detail:Invalid credentials'},status=401)


# class RegisterApiView(APIView):

#     permission_classes = [AllowAny]

#     def post(self,request,*args,**kwargs):

#         if request.user.is_authenticated:
#             return Response({'detail':'You are already authenticated.'},status=400)

#         data = request.data

#         username  = data.get('username')
#         email     = data.get('email')
#         password  = data.get('password')
#         password2  = data.get('password2')


#         if password != password2:
#             return Response({'detail:Password not matched'},status=401)


#         qs = User.objects.filter(
#             Q(username__iexact=username)|
#             Q(email__iexact=username)
#         ).distinct()

#         if qs.exists():

#             return Response({'detail':'The user already exists'},status=401)

#         else:

#             user = User.objects.create(username=username,email=email)

#             user.set_password(password)

#             user.save()

#             # if qs.count() == 1:
#             # user_obj = qs.first()

#             # if user_obj.check_password(password):
#             # user = user_obj

#             payload = jwt_payload_handler(user)
#             token = jwt_encode_handler(payload)
#             response = jwt_response_payload_handler(token,user,request=request)

#             return Response(response)

#         return Response({'detail:Invalid credentials'},status=401)

class RegisterApiView(generics.CreateAPIView):

    queryset = User.objects.all()
    permission_classes = [UserPermission]
    serializer_class = userSerializer

    def get_serializer_context(self,*args,**kwargs):

        return {'request':self.request}


class UserDetailView(generics.RetrieveAPIView):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserStatusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'username'

    def get_serializer_context(self,*args,**kwargs):

        return {'request':self.request}

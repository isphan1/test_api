from django.urls import path,include
from rest_framework_jwt.views import refresh_jwt_token,obtain_jwt_token
from accounts import views

urlpatterns = [
    path("",views.AuthApiView.as_view()),
    path("user/<str:username>",views.UserDetailView.as_view()),
    path("register",views.RegisterApiView.as_view()),
    path('jwt',obtain_jwt_token),
    path('jwt/refresh',refresh_jwt_token),
]
from django.urls import path,include
from accounts.views import UserDetailView

app_name = 'api-user'

urlpatterns = [
    path("<str:username>/",UserDetailView.as_view(),name='detail'),
]
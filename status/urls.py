from django.urls import path
from status import views

urlpatterns = [
    path('',views.statusListAPIView.as_view()),
    # path('create',views.statusCreateAPIView.as_view()),
    path('<int:id>',views.statusDetailAPIView.as_view()),
    # path('<int:pk>/update',views.statusUpdateAPIView.as_view()),
    # path('<int:pk>/delete',views.statusDeleteAPIView.as_view()),

]
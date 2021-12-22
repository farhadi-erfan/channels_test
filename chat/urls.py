from django.conf.urls import url
from django.urls import path, include
import notifications.urls
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import Login

urlpatterns = [
    # path('', views.index, name='index'),
    # path('room/', views.room, name='room'),
]

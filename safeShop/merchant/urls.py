from django.contrib import admin
from django.urls import path,include,re_path
from .views import *

# from knox import views as knox_views
from knox import views as knox_views
app_name = 'merchant'

from rest_framework import routers
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'customerprofile', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('validate_phone/',ValidatePhoneSendOTP.as_view()),
    path('validate_otp/',ValidateOTP.as_view()),
    path('register/',Register.as_view()),
    path('login/',LoginAPI.as_view()),
    path('logout/',LogoutView.as_view()),
    path('logout/',knox_views.LogoutView.as_view()),
    # re_path('^customerprofile/',CustomerProfile.as_view())



   
]
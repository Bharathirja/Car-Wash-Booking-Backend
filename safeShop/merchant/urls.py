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
    re_path('^validate_phone/',ValidatePhoneSendOTP.as_view()),
    re_path('^validate_otp/',ValidateOTP.as_view()),
    re_path('^register/',Register.as_view()),
    re_path('^login/',LoginAPI.as_view()),
    re_path('^logout/',LogoutView.as_view()),
    re_path('^logout/$',knox_views.LogoutView.as_view()),
    # re_path('^customerprofile/',CustomerProfile.as_view())



   
]
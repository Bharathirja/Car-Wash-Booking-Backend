app_name = 'customer'
from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework import routers
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'customer-profile', CustomerViewSet)
router.register(r'vehicle-brand',VehicleViewSet)
router.register(r'bookings',BookingViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('validate-email/',SendEmail.as_view()),# Email sending
    path('validate-otp/',ValidateEmailOTP.as_view()), # Validate OTP
    path('logout/',LogoutView.as_view()), #User logout
]
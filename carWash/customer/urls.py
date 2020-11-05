from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from .auth.user import TokenVerify
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'vehicle-brand', VehicleViewSet)
router.register(r'time-slots', TimeSlotsViewSet)
router.register(r'area', AreaViewSet)
app_name = 'customer'


urlpatterns = [
    path('', include(router.urls)),
    path('validate-email/', SendEmail.as_view(), name='validate-email'),  # Email sending
    path('validate-otp/', ValidateEmailOTP.as_view(), name='validate-otp'),  # Validate OTP
    path('time-slots-available/', SlotChoose.as_view()),

    path('bookings/', BookingAPIView.as_view()),
    path('customer-profile/', CustomerProfileView.as_view()),
    path('customer-profile/<str:email>/', CustomerProfileView.as_view()),

    path('logout/', LogoutView.as_view(), name='logout'),      # User logout
    path('token-verify/', TokenVerify.as_view(), name='logout'),  # User Token Verify
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

]

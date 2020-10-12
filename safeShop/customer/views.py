

from .models import CustomerProfile,VehicleBrand,Bookings
from .serializer import *
from rest_framework import permissions, status, generics,viewsets
from .auth.user import SendEmail,ValidateEmailOTP,LogoutView

from rest_framework.response import Response


'''Customer Profile Views'''
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = VehicleBrand.objects.all()
    serializer_class = VehicleBrandSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer

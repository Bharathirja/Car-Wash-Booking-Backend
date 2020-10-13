

from .models import CustomerProfile,VehicleBrand,Bookings
from customer.serializer import *
from rest_framework import permissions, status, generics,viewsets
from .auth.user import SendEmail,ValidateEmailOTP,LogoutView
from rest_framework.permissions import IsAuthenticated, AllowAny



'''Customer Profile Views'''
class CustomerViewSet(viewsets.ModelViewSet):

    permission_classes = [ IsAuthenticated ]
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerSerializer

    def perform_create(self,serializer):
        serializer.save(user = self.request.user, email =  self.request.user.email)


class VehicleViewSet(viewsets.ModelViewSet):

    permission_classes = [ IsAuthenticated ]
    queryset = VehicleBrand.objects.all()
    serializer_class = VehicleBrandSerializer

    def perform_create(self,serializer):
        serializer.save(user = self.request.user)

class BookingViewSet(viewsets.ModelViewSet):
    
    permission_classes = [ IsAuthenticated ]
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self,serializer):
        serializer.save(user = self.request.user)

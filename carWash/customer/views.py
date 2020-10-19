

from .models import CustomerProfile,VehicleBrand,Bookings
from .serializer import *
from rest_framework import permissions, status, generics,viewsets
from .auth.user import SendEmail,ValidateEmailOTP,LogoutView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

'''Vehicle Brand viewsets'''
class VehicleViewSet(viewsets.ModelViewSet):

    permission_classes = [ IsAuthenticated ]
    queryset = VehicleBrand.objects.all()
    serializer_class = VehicleBrandSerializer

    def perform_create(self,serializer):
        serializer.save(created_user = self.request.user)

'''Time slots viewsets'''
class TimeSlotsViewSet(viewsets.ModelViewSet):
    
    permission_classes = [ IsAuthenticated ]
    queryset = TimeSlots.objects.filter(active=True)
    serializer_class = TimeSlotsSerializer

    def perform_create(self,serializer):
        serializer.save(created_user = self.request.user)

'''Area viewsets'''
class AreaViewSet(viewsets.ModelViewSet):
    
    permission_classes = [ IsAuthenticated ]
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    def perform_create(self,serializer):
        serializer.save(created_user = self.request.user)

'''Bookings Brand viewsets'''
class BookingViewSet(viewsets.ModelViewSet):
    
    permission_classes = [ IsAuthenticated ]
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self,serializer):
        serializer.save(created_user = self.request.user)

'''Customer Profile Views'''
class CustomerViewSet(viewsets.ModelViewSet):

    permission_classes = [ IsAuthenticated ]
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        self.queryset = CustomerProfile.objects.filter(created_user = self.request.user)
        return self.queryset

    def perform_create(self,serializer):
        serializer.save(created_user = self.request.user, email =  self.request.user.email)

'''Login viewset'''
class LoginView(TokenObtainPairView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

from ..models import VehicleBrand,Bookings,Area
from ..serializer import *
from rest_framework import permissions, status, generics,viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

class VehicleViewSet(viewsets.ModelViewSet):
    '''
    Vehicle Brand viewsets
    '''
    permission_classes = [ IsAuthenticated ]
    queryset = VehicleBrand.objects.all()
    serializer_class = VehicleBrandSerializer

    def perform_create(self,serializer):
        serializer.save(created_user = self.request.user)
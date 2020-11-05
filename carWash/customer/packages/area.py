from ..models import VehicleBrand,Bookings,Area
from ..serializer import *
from rest_framework import permissions, status, generics,viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny


class AreaViewSet(viewsets.ModelViewSet):
    '''
    Area viewsets
    '''
    permission_classes = [ IsAuthenticated ]
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    def perform_create(self,serializer):
        serializer.save(created_user = self.request.user)
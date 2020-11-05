from ..models import VehicleBrand,TimeSlots,Bookings
from ..serializer import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets

class TimeSlotsViewSet(viewsets.ModelViewSet):
    '''
    Time slots viewsets
    '''
    permission_classes = [ IsAuthenticated ]
    queryset = TimeSlots.objects.all()
    serializer_class = TimeSlotsSerializer
    

    def perform_create(self,serializer):
        serializer.save(created_user = self.request.user)
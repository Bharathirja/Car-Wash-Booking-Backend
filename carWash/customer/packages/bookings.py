
from ..models import CustomerProfile,VehicleBrand,Bookings
from ..serializer import *
from rest_framework import permissions, status, generics,viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from datetime import datetime as dt
from django.db.models import Q,Sum,F
from rest_framework.views import APIView
from django.http.response import Http404
from .temp_data import booking_temprory
from datetime import datetime
from datetime import date
now = datetime.now()
today = date.today()

class BookingAPIView(APIView):
    '''
    Bookings Brand viewsets
    '''
    permission_classes = [ IsAuthenticated ]
    
    def get_object(self, email):
        try:
            # print(email)
            return Bookings.objects.get(created_user=self.request.user)
        except Bookings.DoesNotExist:
            raise  Http404

    def get(self, request, format=None):

        try:
            bookings = Bookings.objects.filter(created_user = self.request.user).values('pk',
                'vehicle_type','slot__slot','date','area','longitude','latitude','longitude_delta','latitude_delta','booking_amount','completed')
            return Response(list(bookings),status=status.HTTP_200_OK)
        except Exception as  err:
            return Response({'detail':str(err)})
    
    def post(self, request, format=None):
        try:
            data = booking_temprory(request.data)
            serializer = BookingSerializer(data=data)
            if serializer.is_valid():
                serializer.save(created_user = self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'detail':str(err),}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, email, format=None):
        customer = self.get_object(email)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class SlotChoose(APIView):
    '''
    Time slots load depends by already booked date
    '''
    permission_classes = [ IsAuthenticated ]
    def post(self, request):

        try:
            date = dt.strptime(request.data['date'], "%b %d %Y")  # Oct 21 2020
            this_day = today.strftime("%b %d %Y")
            available_slots = Bookings.objects.filter(Q(date=date) & Q(completed=False)).values('slot')
            slot = TimeSlots.objects.filter(~Q(pk__in=available_slots)).values('pk','slot',)
            if request.data['date'] == this_day:
                current_time = now.strftime("%I:%M %p")
                convert_slot_hour = current_time[:3] + '00'
                # print(convert_slot_hour)
                return Response({'detail':today_slot_available(slot, convert_slot_hour)})
            return Response({'detail':list(slot)})
        except IndexError:
            # print('varuthu')
            return Response({'detail':[]})
        except Exception as err:
            return Response({'detail':str(err)})

def today_slot_available(slots, convert_slot_hour):
    # try:
    today_availablity = [ slots[i+2] for i, value  in enumerate(slots) if slots[i]['slot'].find(convert_slot_hour) >= 0 ]
        # print(today_availablity)
    return today_availablity
    # except Exception as err:
    #     print('Inga varuthu')
    #     return Response({'detail':str(err)})
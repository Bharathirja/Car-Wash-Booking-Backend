

from .models import CustomerProfile
from .serializer import *
from rest_framework import permissions, status, generics,viewsets
from .auth.user import SendEmail,ValidateEmailOTP,LogoutView

'''Customer Profile Views'''
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerSerializer



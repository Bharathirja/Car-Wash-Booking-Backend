from django.shortcuts import render
from django.http import HttpResponse
import random
from django.core.mail import send_mail
from ..serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password    
from rest_framework.generics import get_object_or_404
from django.http.response import Http404
from ..models import User, EmailOTP


def send_otp(phone):
    """Generate Random 4 digit number"""
    if phone:
        key = random.randint(999, 9999)
        return key
    else:
        return False


class SendEmail(APIView):
    """
    Create your views here.Send Verification
    code to user email
    """
    @staticmethod
    def get(request):
        data = EmailOTP.objects.filter(validated=True)
        serializer = EmailOTPSerializer(data, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        try:
            email_address = request.data.get('email')
            if email_address:
                email = str(email_address)
                key = send_otp(email)
                if key:
                    old = EmailOTP.objects.filter(email__iexact=email)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        old.count = count + 1
                        old.otp = key
                        old.active = True
                        old.validated = False
                        old.save()

                        # Email Sending
                        send_mail(
                            "Verifications",  # Subject
                            "Your Verification OTP is " + str(key),  # Body of mail
                            "bharathiraja@pganalytics.in",  # from mail
                            [email_address],)  # To mail
                        return Response({'detail': 'OTP sent successfully'}, status=status.HTTP_200_OK)
                    else:
                        EmailOTP.objects.create(email=email, otp=key)

                        # Email Sending
                        send_mail(
                            "Verifications",
                            "Your Verification OTP is " + str(key),
                            "bharathiraja@pganalytics.in",
                            [email_address],)
                        return Response({'detail': 'OTP sent successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Sending OTP error'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Email is not given'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)


class ValidateEmailOTP(APIView):
    """
    Validate OTP and create new user
    """
    @staticmethod
    def post(request, **kwargs):

        try:
            email = request.data.get("email", False)
            otp_sent = request.data.get('otp', False)

            if email and otp_sent:
                
                old = EmailOTP.objects.filter(email__iexact=email)
                if old.exists():
                    old = old.first()
                    check = old.otp == otp_sent
                    if check:
                        old.validated = True
                        old.save()
                        exist_user = User.objects.filter(email__iexact=email)
                        if exist_user.exists():
                            user = User.objects.get(email=email)
                            profile = CustomerProfile.objects.get(email = user)
                            token, created = Token.objects.get_or_create(user=user)
                            # customer_name = CustomerProfile.objects.get(created_user = user.pk)
                            return Response({'detail': 'OTP MATCHED', 'token': token.key, 'exist':True, 'name': profile.name, 'photo': "/media/"+str(profile.photo)})
                        User.objects.create_user(email=email, password=otp_sent)
                        user = User.objects.get(email=email)
                        token, created = Token.objects.get_or_create(user=user)
                        return Response({'detail': 'OTP MATCHED', 'token': token.key, 'exist': False})
                    return Response({'detail': 'OTP MISMATCHED'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'detail': 'OTP OR EMAIL MISMATCHED.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'Please provide both Email and OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    """
    User Logout
    """
    @staticmethod
    def post(request):
        user_token = request.data['token']
        try:
            if user_token:
                token = get_object_or_404(Token, key=request.data["token"])
                email = token.user
                user = get_object_or_404(User, email=email)
                
                user.save()
                token.delete()
                EmailOTP.objects.filter(email=email).update(validated=False)
                return Response({'detail': 'User logged out successfully'}, status=status.HTTP_200_OK)
            return Http404
        except Token.DoesNotExist:
            raise Http404

  
class TokenVerify(APIView):
    """
    Token verifying
    """
    @staticmethod
    def post(request):
        try:
            get_object_or_404(Token, key = request.data["token"])
            return Response({"detail":"success"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)})


class LoginView(TokenObtainPairView):
    """
    Login viewset
    """
    queryset = User.objects.all()
    serializer_class = LoginSerializer
from django.shortcuts import render
from django.http import HttpResponse
import random
from django.core.mail import send_mail
from ..serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics,viewsets
from ..models import User, EmailOTP
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import login,logout

'''Generate Random 4 digit number'''
def send_otp(phone):
    if phone:
        key = random.randint(999,9999)
        print(key)
        return key
    else:
        return False
        
    
'''Create your views here.Send Verification 
code to user email'''
class SendEmail(APIView):
    def post(self,request):
        try:
            email_address = request.data.get('email')
            if email_address:
                email = str(email_address)
                user = User.objects.filter(email__iexact = email)
                if user.exists():
                    return Response({'detail': 'Email already exists'},status = status.HTTP_226_IM_USED)
                else:
                    key = send_otp(email)
                    if key:
                        old = EmailOTP.objects.filter(email__iexact = email,active=True)
                        if old.exists():
                            old = old.first()
                            count = old.count
                            if count > 100:
                                return Response({'status' : False,'detail' : 'Limit Exceeded'})
                            old.count = count +1
                            old.otp = key
                            old.active = True
                            old.validated = False
                            old.save()

                            # Email Sending
                            send_mail('Verifications',
                            'Your Verification OTP is '+ str(key),
                            'bharathiraja.pappugroup@gmail.com',
                            [email_address],)

                            return Response({'detail' : 'OTP sent successfully'},status=status.HTTP_200_OK)
                        else:
                            EmailOTP.objects.create(email = email,otp = key)

                            # Email Sending
                            send_mail('Verifications',
                            'Your Verification OTP is '+ str(key), 
                            'bharathiraja.pappugroup@gmail.com',
                            [email_address],)

                            return Response({'detail' : 'OTP sent successfully'},status=status.HTTP_200_OK)
                    else:
                        return Response({'detail' : 'Sending OTP error'},status=status.HTTP_408_REQUEST_TIMEOUT)   
            else:
                return Response({'detail' : 'Email is not given'},status=status.HTTP_204_NO_CONTENT) 
        except Exception as err:
            return Response({'detail' : str(err)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



'''Validate OTP and create new user'''
class ValidateEmailOTP(APIView):

    def post(self, request, **kwargs):

        try:
            email = request.data.get("email", False)
            otp_sent = request.data.get('otp', False)

            if email and otp_sent:
                old = EmailOTP.objects.filter(email__iexact = email,active=True)
                if old.exists():
                    old = old.first()
                    check = old.otp == otp_sent
                    if check:
                        old.validated = True
                        old.save()
                        User.objects.create(email = email,password = int(otp_sent))
                        user = User.objects.get(email=email)
                        token, created = Token.objects.get_or_create(user=user)

                        return Response({
                            'detail' : 'OTP MATCHED.',
                            'token' : token.key,
                            'user_id':token.user.pk 
                            })
                    return Response({'detail' : 'OTP MISMATCHED.'},status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({'detail' : 'Please provide both Email and OTP'},status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as err:
            return Response({'detail':str(err)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



'''User Logout'''
class LogoutView(APIView):

    def post(self,request):
        user_id = request.data['user_id']
        try:
            if user_id:
                user = User.objects.get(pk = user_id)
                user_phone = user.email
                user.delete()
                EmailOTP.objects.filter(email=user_phone).update(active=False,validated = False)
                return Response({'detail':'User logged out successfully'},status=status.HTTP_200_OK)
            return Response({'detail' : 'User not found'},status=status.HTTP_204_NO_CONTENT)   
        except Exception as err:
            return Response({'detail':str(err)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




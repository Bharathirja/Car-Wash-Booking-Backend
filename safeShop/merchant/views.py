

from django.shortcuts import render
from django.http import HttpResponse
import http.client
# Create your views here.
import json
import requests
import ast

from .models import CustomerProfile
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics,viewsets
# from forms import UserForm
from .models import User, PhoneOTP
from django.shortcuts import get_object_or_404, redirect
import random
from .serializer import CreateUserSerializer, LoginSerializer
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import login,logout

conn = http.client.HTTPConnection("2factor.in")
from rest_framework.authtoken.models import Token

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerSerializer

class ValidatePhoneSendOTP(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        # password = request.data.get('password', False)
        # username = request.data.get('username', False)
        # email    = request.data.get('email', False)

        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({
                    'status' : False,
                    'detail' : 'Phone number already exists'
                })

            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 10:
                            return Response({
                                'status' : False,
                                'detail' : 'Sending otp error. Limit Exceeded. Please Contact Customer support'
                            })

                        old.count = count +1
                        old.otp = key
                        old.active = True
                        old.save()
                        print('Count Increase', count)

                        conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=094ba169-ec1d-11ea-9fa5-0200cd936042&to="+phone+"&otpvalue="+str(key)+"&templatename=SafeShop")
                        res = conn.getresponse() 
                       
                        data = res.read()
                        data=data.decode("utf-8")
                        data=ast.literal_eval(data)
                        
                        print(data)
                        if data["Status"] == 'Success':
                            old.otp_session_id = data["Details"]
                            old.save()
                            # user = User.objects.create(phone = phone,password = int(key))
                            # user_id = user.pk
                            
                            print('In validate phone :'+old.otp_session_id)
                            return Response({
                                   'status' : True,
                                   'detail' : 'OTP sent successfully',
                                })    
                        else:
                            return Response({
                                  'status' : False,
                                  'detail' : 'OTP sending Failed'
                                }) 

                       


                    else:

                        obj=PhoneOTP.objects.create(
                            phone=phone,
                            otp = key,
                            # email=email,
                            # username=username,
                            # password=password,
                        )
                        conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=094ba169-ec1d-11ea-9fa5-0200cd936042&to="+phone+"&otpvalue="+str(key)+"&templatename=SafeShop")
                        res = conn.getresponse()    
                        data = res.read()
                        # print(data.decode("utf-8"))
                        data=data.decode("utf-8")
                        data=ast.literal_eval(data)
                        print(data)

                        if data["Status"] == 'Success':
                            obj.otp_session_id = data["Details"]
                            obj.save()
                            
                            print('In validate phone :'+obj.otp_session_id)
                            return Response({
                                   'status' : True,
                                   'detail' : 'OTP sent successfully'
                                })    
                        else:
                            return Response({
                                  'status' : False,
                                  'detail' : 'OTP sending Failed'
                                })

                        
                else:
                     return Response({
                           'status' : False,
                            'detail' : 'Sending otp error'
                     })   

        else:
            return Response({
                'status' : False,
                'detail' : 'Phone number is not given in post request'
            })            



def send_otp(phone):
    if phone:
        key = random.randint(999,9999)
        print(key)
        return key
    else:
        return False


class LogoutView(APIView):
    def post(self,request):
        user_id = request.data['user_id']
        print(user_id)
        try:
            if user_id:
                print(user_id)
                user = User.objects.get(pk = user_id)
                print(user)
                user_phone = user.phone
                user.delete()
                PhoneOTP.objects.filter(phone=user_phone).update(active=False)

                return Response({'status':True,'detail':'User logged out successfully'})

            return Response({
                'status' : False,
                'detail' : 'user not found'})   
        except Exception as err:
            return Response({
                "status":False,
                "detail":str(err)
            })


class ValidateOTP(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)


        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp_session_id = old.otp_session_id
                print("In validate otp"+otp_session_id)
                conn.request("GET", "https://2factor.in/API/V1/094ba169-ec1d-11ea-9fa5-0200cd936042/SMS/VERIFY/"+otp_session_id+"/"+otp_sent)
                res = conn.getresponse()   
                print(res) 
                data = res.read()
                print(data.decode("utf-8"))
                data=data.decode("utf-8")
                data=ast.literal_eval(data)
                
                

                if data["Status"] == 'Success':
                    old.validated = True
                    old.save()
                    User.objects.create(phone = phone,password = int(otp_sent))
                    user = User.objects.get(phone=phone)
                    token,created = Token.objects.get_or_create(user=user)
                    print(token)
                
                    
                    return Response({
                        'status' : True,
                        'detail' : 'OTP MATCHED.',
                        'token' : token.key,
                        'user_id':token.user.pk
                        })

                else:
                    return Response({
                        'status' : False,
                        'detail' : 'OTP INCORRECT'
                    })
                


            else:
                return Response({
                        'status' : False,
                        'detail' : 'First Proceed via sending otp request'
                    })


        else:
            return Response({
                        'status' : False,
                        'detail' : 'Please provide both phone and otp for Validation'
                    })





class Register(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        # password = request.data.get('password', False)
        # username = request.data.get('username', False)
        # email    = request.data.get('email', False)


        if phone:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                validated = old.validated

                if validated:
                        temp_data = {
                            # 'username' : old.username,
                            # 'email' :old.email,
                            'phone' : old.phone,
                            # 'password' : password,
                         
                        }
                        print(temp_data)
                        serializer = CreateUserSerializer(data = temp_data)
                        serializer.is_valid(raise_exception = True)
                        user = serializer.save()
                        # user.set_password(password)
                        user.save()
                        print(user)
                        # print(password)
                        old.delete()
                        return Response({
                            'status' : True,
                            'detail' : 'Account Created Successfully'
                            })   

                else:
                    return Response({
                        'status' : False,
                        'detail' : 'OTP havent Verified. First do that Step.'
                        })


            else:    
                return Response({
                'status' : False,
                'detail' : 'Please verify Phone First'
            })   
        else:
            return Response({
                'status' : False,
                'detail' : 'Both username, email, phone, password are not sent'
            })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format = None):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)

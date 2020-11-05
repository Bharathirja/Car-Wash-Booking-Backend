from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import *
from django.contrib.auth import login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenVerifySerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.models import Token


User = get_user_model()

class EmailOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailOTP
        fields = '__all__'

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)
        extra_kwargs = {'password': {'write_only' : True},}
        
        def create(self, validated_data):
            
            user = User.objects.create(**validated_data)
            return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email',)


class LoginSerializer(serializers.Serializer):
    
    email = serializers.CharField()
    password = serializers.CharField(
        style = { 'input_type': 'password'}, trim_whitespace = False
    )
    
    def validate(self, data):
       
        email = data.get('email')
        password = data.get('password')
        
        if email:
            if User.objects.filter(email = email).exists():
                user = authenticate(request = self.context.get('request'), phone = email,password = password)
            else:
                msg = {
                    'detail' : 'Username number not found',
                    'status' : False,
                }    
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail' : 'Email and password not matching. Try again',
                    'status' : False,
                }    
                raise serializers.ValidationError(msg, code = 'authorization')

        
        else:
            msg = {
                    'detail' : 'Email and password not found in request',
                    'status' : False,
                }    
            raise serializers.ValidationError(msg, code = 'authorization')

        data['user'] = user
        return data

class AreaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Area
        fields = ('pk','area_name',)


class VehicleBrandSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = VehicleBrand
        fields = ('pk','brand_name','amount')


class TimeSlotsSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = TimeSlots
        fields = ('pk','slot','date','active')


class CustomerSerializer(serializers.ModelSerializer):
    
    # email = serializers.CharField(read_only=True)
    class Meta:
        model = CustomerProfile
        fields = ('pk','name','phone','address','photo','email')

class BookingSerializer(serializers.ModelSerializer):

    completed = serializers.CharField(read_only=True)

    class Meta:
        model = Bookings
        fields = (
            'pk','vehicle_type','area','slot','date',
            'completed','booking_amount','longitude',
            'latitude','longitude_delta','latitude_delta')
    

class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        print(self.user)
        refresh = self.get_token(self.user)
        
        token, created = Token.objects.get_or_create(user=self.user)
        # data["token"] = data.pop("access")
        data["id"] = self.user.id
        data["token"] = token.key
        return data

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import *
from django.contrib.auth import login

User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)
        extra_kwargs = {'password': {'write_only' : True},}
        
        def create(self, validated_data):
            print(validated_data)
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

class VehicleBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model=VehicleBrand
        fields=('pk','brand_name')

class BookingSerializer(serializers.ModelSerializer):

    active = serializers.BooleanField(read_only=True)
    class Meta:
        model=Bookings
        fields=('pk','vehicle_type','area','date','slot','longitude','latitude','active')


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerProfile
        fields = ('pk','name','phone','email','address','photo')

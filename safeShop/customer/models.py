from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models.signals import post_save
import random
import os
import requests

class UserManager(BaseUserManager):
   
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('Phone number must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    
    username = None
    email = models.EmailField('Email',max_length=254, unique=True,null=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
class EmailOTP(models.Model):
   
    email = models.EmailField(max_length = 254, unique=True) 
    otp         = models.CharField(max_length=9, blank = True, null=True)
    count       = models.IntegerField(default=0, help_text = 'Number of OTP sent')
    validated   = models.BooleanField(default = False, help_text = 'If it is true, that means user have validate otp correctly in second API')
    active = models.BooleanField(default=True)
    date = models.DateTimeField('date',auto_now_add=True)
    
    def __str__(self):
        return str(self.email) + ' is sent ' + str(self.otp)

class VehicleBrand(models.Model):
    
    TYPES = (('HATCHPACK', 'HATCHPACK'), ('SEDAN', 'SEDAN'), ('SUV', 'SUV'),)
    brand_name = models.CharField(max_length=250,choices=TYPES)
    date = models.DateTimeField('date',auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='vehicle_user')

    def __str__(self):
        return str(self.brand_name)


class Bookings(models.Model):

    vehicle_type = models.ForeignKey(VehicleBrand,on_delete=models.PROTECT,related_name='vehicle_types')
    area = models.CharField('area',max_length=250)
    date = models.DateField('date')
    slot = models.CharField('slot',max_length=250)
    active = models.BooleanField('active',default=True)
    longitude = models.DecimalField('longitude',max_digits=9, decimal_places=6)
    latitude  = models.DecimalField('latitude',max_digits=9, decimal_places=6)
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='booking_user')

    def __str__(self):
        return str(self.vehicle_type)



class CustomerProfile(models.Model):

    phone_regex = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
    phone       = models.CharField('Phone',validators =[phone_regex], max_length=10, unique = True,null=True)
    name = models.CharField(max_length=250,null=False,blank=False)
    email = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    photo = models.ImageField(upload_to='customers/')
    date = models.DateTimeField('date',auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='customer_user')


    def __str__(self):
        return "{}".format(self.name)

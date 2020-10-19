
# Register your models here.
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib import admin
User = get_user_model()

from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

'''Custom user'''
class CustomUserAdmin(BaseUserAdmin):

    add_form = CustomUserCreationForm
    model = User
    list_display = ('pk','email','is_staff', 'is_active',)
    list_filter = ('email','is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
       
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2','is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

'''Email and OTP'''
class EmailOTPAdmin(admin.ModelAdmin):

    model = EmailOTP
    list_display = ('pk','email','otp','validated','active','created_at',)
    list_display_links = ('email',)
    list_filter = ('email','validated','created_at')
   
    search_fields = ('email','created_at')
    ordering = ('email',)

'''Vehicle brand'''
class VehicleBrandAdmin(admin.ModelAdmin):

    model = VehicleBrand
    list_display = ('pk','brand_name','amount','created_at','created_user')
    list_display_links = ('brand_name',)
    list_filter = ('brand_name','amount')
   
    search_fields = ('brand_name','amount','created_at')
    ordering = ('brand_name','amount')

'''Time slots'''
class TimeSlotsAdmin(admin.ModelAdmin):
    
    model = TimeSlots
    list_display = ('pk','slot','active','created_at')
    list_display_links = ('slot',)
    list_filter = ('slot',)
   
    search_fields = ('slot',)
    ordering = ('slot','created_at',)

'''Area'''
class AreaAdmin(admin.ModelAdmin):
    
    model = Area
    list_display = ('pk','area_name','created_at')
    list_display_links = ('area_name',)
    list_filter = ('area_name',)
   
    search_fields = ('area_name',)
    ordering = ('area_name','created_at',)

'''Bookings'''
class BookingsAdmin(admin.ModelAdmin):
    
    model = VehicleBrand
    list_display = ('pk','vehicle_type','area','slot','booking_amount','longitude','latitude','completed','created_user','created_at')
    list_display_links = ('vehicle_type',)
    list_filter = ('vehicle_type','area','booking_amount','created_at','slot')
   
    search_fields = ('vehicle_type','slot','booking_amount')
    ordering = ('vehicle_type','booking_amount','created_at')

'''Customer profile'''
class CustomerProfileAdmin(admin.ModelAdmin):
    
    model = CustomerProfile
    list_display = ('pk','phone','name','address','photo','created_at','created_user')
    list_display_links = ('phone',)
    list_filter = ('phone','name')
   
    search_fields = ('phone','name')
    ordering = ('name','phone')


'''Model registrations to admin panel'''

admin.site.register(User, CustomUserAdmin)
admin.site.register(EmailOTP, EmailOTPAdmin)
admin.site.register(VehicleBrand,VehicleBrandAdmin)
admin.site.register(TimeSlots,TimeSlotsAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(Bookings,BookingsAdmin)
admin.site.register(CustomerProfile,CustomerProfileAdmin)



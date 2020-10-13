
# Register your models here.
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib import admin
User = get_user_model()

from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import EmailOTP,CustomerProfile,VehicleBrand,Bookings

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

class EmailOTPAdmin(admin.ModelAdmin):

    model = EmailOTP
    list_display = ('pk','email','validated','active','created_at',)
    list_display_links = ('email',)
    list_filter = ('email','validated','created_at')
   
    search_fields = ('email','created_at')
    ordering = ('email',)

class CustomerProfileAdmin(admin.ModelAdmin):


    model = CustomerProfile
    list_display = ('pk','phone','name','address','photo','created_at','user')
    list_display_links = ('phone',)
    list_filter = ('phone','name')
   
    search_fields = ('phone','name')
    ordering = ('name','phone')

class VehicleBrandAdmin(admin.ModelAdmin):

    model = VehicleBrand
    list_display = ('pk','brand_name','created_at','user')
    list_display_links = ('brand_name',)
    list_filter = ('brand_name',)
   
    search_fields = ('brand_name','created_at')
    ordering = ('brand_name',)

class BookingsAdmin(admin.ModelAdmin):
    
    model = VehicleBrand
    list_display = ('pk','vehicle_type','area','date','slot','longitude','latitude','active','user','created_at')
    list_display_links = ('vehicle_type',)
    list_filter = ('vehicle_type','area','created_at','slot')
   
    search_fields = ('vehicle_type','slot')
    ordering = ('vehicle_type','created_at')

admin.site.register(Bookings,BookingsAdmin)
admin.site.register(CustomerProfile,CustomerProfileAdmin)
admin.site.register(EmailOTP, EmailOTPAdmin)
admin.site.register(VehicleBrand,VehicleBrandAdmin)
admin.site.register(User, CustomUserAdmin)

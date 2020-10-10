
# Register your models here.
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib import admin
User = get_user_model()

from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import EmailOTP,CustomerProfile




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
            'fields': ('email','is_staff', 'is_active')}
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
    list_display = ('pk','email','validated','active')
    list_display_links = ('email',)
    list_filter = ('email','validated')
   
    search_fields = ('email',)
    ordering = ('email',)

class CustomerProfileAdmin(admin.ModelAdmin):

    
    model = CustomerProfile
    list_display = ('pk','phone','name','email','address','photo')
    list_display_links = ('email',)
    list_filter = ('email','phone','name')
   
    search_fields = ('email','phone','name')
    ordering = ('name','email','phone')

admin.site.register(CustomerProfile,CustomerProfileAdmin)
admin.site.register(EmailOTP, EmailOTPAdmin)
admin.site.register(User, CustomUserAdmin)

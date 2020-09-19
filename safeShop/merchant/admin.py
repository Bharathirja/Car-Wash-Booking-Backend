
# Register your models here.
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib import admin
User = get_user_model()

from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .forms import UserAdminCreationForm, UserAdminChangeForm

from .models import PhoneOTP,CustomerProfile
admin.site.register(PhoneOTP)
admin.site.register(CustomerProfile)


class CustomUserAdmin(BaseUserAdmin):

    add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = User
    list_display = ('pk','phone','is_staff', 'is_active',)
    list_filter = ('phone','is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('phone','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
       
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone','is_staff', 'is_active')}
        ),
    )
    search_fields = ('phone',)
    ordering = ('phone',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, CustomUserAdmin)

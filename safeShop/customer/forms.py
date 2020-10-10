from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from .models import User,UserManager


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        class Meta(UserCreationForm.Meta):
            model = User
            fields = ('email',)
   
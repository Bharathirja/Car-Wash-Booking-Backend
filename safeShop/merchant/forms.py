from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from .models import User,UserManager


class CustomUserCreationForm(UserCreationForm):
    

    class Meta:
        class Meta(UserCreationForm.Meta):
            model = User
            fields = ('phone',)
    # def __init__(self, *args, **kwargs):
    #     super(CustomUserCreationForm, self).__init__(*args, **kwargs)
    #     self.fields['password1'].required = False
    #     self.fields['password2'].required = False
    #     # If one field gets autocompleted but not the other, our 'neither
    #     # password or both password' validation will be triggered.
    #     self.fields['password1'].widget.attrs['autocomplete'] = 'off'
    #     self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = super(CustomUserCreationForm, self).clean_password2()
    #     if bool(password1) ^ bool(password2):
    #         raise forms.ValidationError("Fill out both fields")
    #     return password2
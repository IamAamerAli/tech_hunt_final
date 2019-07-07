from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import forms

from users.models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# region UserInformation for not for use just for testing
# class UserInformation(forms.Form):
#     gender_choice = [('male', 'Male'), ('female', 'Female'), ('notconfirm', 'Not Confirm')]
#     name = forms.CharField(max_length=50)
#     country_code = forms.CharField(max_length=4, help_text='for example +123, add plus sign before country code')
#     mobile = forms.CharField(max_length=10)
#     email = forms.EmailField()
#     address = forms.CharField(widget=forms.Textarea)
#     gender = forms.ChoiceField(choices=gender_choice, widget=forms.RadioSelect)
#     dob = forms.DateTimeInput()
# endregion


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

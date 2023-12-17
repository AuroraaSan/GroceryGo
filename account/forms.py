from django import forms
from django.contrib.auth.models import User
from .models import Profile
from phonenumber_field.formfields import PhoneNumberField

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'First name'}))
#user model
class UserRegistrationForm(forms.ModelForm):
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Phone number'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}))
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Repeat Password'}))




    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'phone_number']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
# allow users to edit their first name, last name, and email
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
#allow users to edit the profile data 
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'phone_number', 'address']

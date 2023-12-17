from django import forms
from django.contrib.auth.models import User
from .models import Profile, Address
from phonenumber_field.formfields import PhoneNumberField


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
#user model
class UserRegistrationForm(forms.ModelForm):
    address = forms.CharField(max_length=255)
    phone_number = PhoneNumberField()
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)




    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']

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


from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    address = forms.CharField(max_length=255, required=False)  # Add an address field

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'phone_number', 'address']  # Include the address field

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

            # Set initial value for address
            if hasattr(user, 'profile') and user.profile.address:
                self.fields['address'].initial = user.profile.address

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        user = self.instance.user

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        # Update the address field in the profile
        profile.address = self.cleaned_data['address']

        if commit:
            user.save()
            profile.save()

        return profile

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'postal_code', 'country']


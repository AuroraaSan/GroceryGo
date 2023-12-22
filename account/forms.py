""" Account app forms """


from django import forms
from django.contrib.auth.models import User
from .models import Profile, Address
from phonenumber_field.formfields import PhoneNumberField
from django import forms
from .models import Profile


class LoginForm(forms.Form):
    """
    Form for user login.

    Fields:
    - username: User's username for authentication.
    - password: User's password for authentication.
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )


# user model
class UserRegistrationForm(forms.ModelForm):
    """
    Form for user registration.

    Extends ModelForm for the User model and includes additional fields:
    - first_name: User's first name.
    - last_name: User's last name.
    - email: User's email address.
    - date_of_birth: User's date of birth.
    - phone_number: User's phone number.
    - address: User's address.
    - password: User's password.
    - password2: Confirmation of the password.
    """

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First name"}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last name"}
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "placeholder": "Birth date"}
        )
    )
    phone_number = PhoneNumberField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Phone number"}
        )
    )
    street = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Street"}
        ),
    )
    city = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
    )
    postal_code = forms.IntegerField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Postal Code"}
        )
    )
    country = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Country"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Repeat Password"}
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "street",
            "city",
            "postal_code",
            "country",
        ]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]


# allow users to edit their first name, last name, and email
class UserEditForm(forms.ModelForm):
    """
    Form for users to edit their basic information.

    Extends ModelForm for the User model and includes fields:
    - first_name: User's first name.
    - last_name: User's last name.
    - email: User's email address.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


# allow users to edit the profile data
class ProfileEditForm(forms.ModelForm):
    """
    Form for users to edit their profile information.

    Extends ModelForm for the Profile model and includes fields:
    - date_of_birth: User's date of birth.
    - phone_number: User's phone number.
    - address: User's address.
    """

    class Meta:
        model = Profile
        fields = ["date_of_birth", "phone_number"]


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for users to update their profile information, including user data.

    Extends ModelForm for the Profile model and includes additional fields:
    - first_name: User's first name.
    - last_name: User's last name.
    - email: User's email address.
    - address: User's address.

    Provides initial values based on the existing user data and updates both User and Profile instances on save.
    """

    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ["date_of_birth", "phone_number"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        user = self.instance.user

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        # Update the address field in the profile
        profile.address = self.cleaned_data["address"]

        if commit:
            user.save()
            profile.save()

        return profile


class AddressForm(forms.ModelForm):
    """
    Form for collecting and updating address information.

    Extends ModelForm for the Address model and includes fields:
    - street: Street address.
    - city: City name.
    - postal_code: Postal code.
    - country: Country name.
    """

    class Meta:
        model = Address
        fields = ["street", "city", "postal_code", "country"]

from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Address(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="addresses"
    )
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.postal_code}, {self.country}"

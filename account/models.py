from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=255, default='Default Address')


    def __str__(self):
        return f"Profile of {self.user.username}"

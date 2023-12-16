from django.contrib import admin
from .models import Profile,Address
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'phone_number', 'address']
    raw_id_fields = ['user']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['profile', 'street', 'city', 'postal_code', 'country']
    search_fields = ['profile__user__username', 'city']
    list_filter = ['country']

from django.contrib import admin
from .models import Profile,Address
# Register models
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Profile model.

    provides an interface for managing Profile instances in the admin panel.

    Attributes:
        list_display (list): display in the list view of profiles.
        raw_id_fields (list): Fields to be displayed as IDs.
    """
    list_display = ['user', 'date_of_birth', 'phone_number', 'address']
    raw_id_fields = ['user']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Address model.

    provides an organized interface for managing Address instances in the admin panel.

    Attributes:
        list_display (list):  display in the list view of addresses.
        search_fields (list): Fields to search for in the admin panel.
        list_filter (list): Fields for which filtering options will be available.
    """
    list_display = ['street', 'city', 'postal_code', 'country']
    search_fields = ['profile__user__username', 'city']
    list_filter = ['country']

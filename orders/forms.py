from django import forms
from .models import Order
from account.models import Address


class OrderCreateForm(forms.ModelForm):
    user_address = forms.ChoiceField(required=False, label='Address')

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'user_address']

    def __init__(self, user, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        if user is not None:
            default_address = getattr(user.profile, 'address', None)
            other_addresses = Address.objects.filter(profile=user.profile)

            address_choices = []
            
            if default_address:
                address_choices.append((default_address, 'Default Address: ' + str(default_address)))
            
            address_choices += [(address.id, f"{address.street}, {address.city}, {address.postal_code}, {address.country}") for address in other_addresses]

            self.fields['user_address'].choices = address_choices

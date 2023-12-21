from django import forms
from .models import Order
from account.models import Address
from shop.models import Company
from django.contrib.auth.models import User
from account.models import Profile

class OrderCreateForm(forms.ModelForm):
    user_address = forms.ModelChoiceField(queryset=Address.objects.none(), required=False, label='Address')
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'user_address']  

    def __init__(self, user, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
    
        if user is not None and hasattr(user, 'profile') and user.profile:
            # default_address = getattr(user.profile, 'address', None)
            # other_addresses = Address.objects.filter(profile=user.profile)

            # Concatenate the default address and other addresses into a single queryset
            profile = Profile.objects.filter(user=user)
            address_queryset = Address.objects.get(profile=profile)
            print("add")

            self.fields['user_address'].queryset = address_queryset
    def get_info(self,request):
            profile = Profile.objects.filter(user=request.user)
            print(profile)
            address_queryset = Address.objects.get(profile=profile)
            print(address_queryset)
            self.fields['user_address'].queryset = profile



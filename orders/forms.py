from django import forms
from .models import Order
from account.models import Address
from django.contrib.auth.models import User
from account.models import Profile

class OrderCreateForm(forms.ModelForm):
    user_address = forms.ModelChoiceField(queryset=Address.objects.none(), required=False, label='Address')


    class Meta:
        model = Order
        fields = ['user_address']

    def __init__(self, user, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.get_info(user)

    def get_info(self, user):
        profile = Profile.objects.get(user=user)
        address_queryset = Address.objects.filter(profile=profile)
        self.fields['user_address'].queryset = address_queryset

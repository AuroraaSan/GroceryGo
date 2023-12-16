from django import forms
from .models import Company

COUNTRY_LIST = [('','All')] + Company.NATIONALITY_CHOICES 

class ProductFilterForm(forms.Form):
    price_min = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Min Price'}))
    price_max = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Max Price'}))
    company = forms.ModelChoiceField(queryset = Company.objects.all(), empty_label="Choose a Company", required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    nationality=forms.ChoiceField(
        widget=forms.Select(),
        choices=COUNTRY_LIST,
        required=False,
    )
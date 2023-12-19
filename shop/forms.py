from django import forms
from .models import Company

COUNTRY_LIST = [('','All')] + Company.NATIONALITY_CHOICES 

class ProductSearchForm(forms.Form):
    search_query = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Search'}))
    search_category=forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control btn btn-secondary dropdown-toggle'}),
        choices=[(1, 'Company'), (2, 'Product')],
        required=False,
    )

class ProductFilterForm(forms.Form):
    price_min = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Min Price'}))
    price_max = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Max Price'}))
    company = forms.ModelChoiceField(queryset = Company.objects.all(), empty_label="Choose a Company", required=False, widget=forms.Select(attrs={'class': 'btn btn-secondary dropdown-toggle'}))
    nationality=forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'btn btn-secondary dropdown-toggle'}),
        choices=COUNTRY_LIST,
        required=False,
    )


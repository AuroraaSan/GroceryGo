from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Product, Category, Company
from django.db.models import Q, Max
from .forms import ProductFilterForm


def product_list(request, category_name=None):
    category = None
    categories = Category.objects.all()

    form = ProductFilterForm(request.GET)
    products = Product.objects.all()
    if category_name:
        category = get_object_or_404(Category, category_name=category_name)
        products = products.filter(Q(cat=category) | Q(cat__parent_cat=category))

    if form.is_valid():
        price_min=form.cleaned_data.get('price_min')
        price_max=form.cleaned_data.get('price_max')
        company=form.cleaned_data.get('company')
        nationality=form.cleaned_data.get('nationality')

        if price_min is None:
            price_min = 0
            
        if price_max is None:
            price_max = products.aggregate(Max('price'))['price__max']

        products = products.filter(price__range=(price_min, price_max))

        if company:
            company_id = company.company_id
            products = products.filter(company_id=company_id)
        
        if nationality:
            company_ids = list(Company.objects.filter(nationality=nationality).values_list('company_id', flat=True))
            products = products.filter(company_id__in=company_ids)

    return render(
        request,
        "shop/product/list.html",
        {"category": category, "categories": categories, "products": products, "form": form},
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, p_id=id, slug=slug)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        "shop/product/detail.html",
        {"product": product, "cart_product_form": cart_product_form},
    )

from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Product, Category, Company
from django.db.models import Q


def product_list(request, category_name=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_name:
        category = get_object_or_404(Category, category_name=category_name)
        products = products.filter(Q(cat=category) | Q(cat__parent_cat=category))
    return render(
        request,
        "shop/product/list.html",
        {"category": category, "categories": categories, "products": products},
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, p_id=id, slug=slug)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        "shop/product/detail.html",
        {"product": product, "cart_product_form": cart_product_form},
    )

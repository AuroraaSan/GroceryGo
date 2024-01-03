from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Product, Category, Company
from django.db.models import Q, Max, Count, F, Case, When, Sum
from .forms import ProductFilterForm, ProductSearchForm
from django.db import models  # Import the models module
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from cart import forms as cart_forms


def product_list(request, category_name=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    filter_form = ProductFilterForm(request.GET)
    search_form = ProductSearchForm(request.GET)
    cart_form = cart_forms.CartAddProductForm(request.POST)

    if category_name:
        category = get_object_or_404(Category, category_name=category_name)
        products = products.filter(Q(cat=category) | Q(cat__parent_cat=category))

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search_query")
        search_category = search_form.cleaned_data.get("search_category")

        if search_category == "1":
            company_search_ids = list(
                Company.objects.filter(
                    company_name__icontains=search_query
                ).values_list("company_id", flat=True)
            )
            products = products.filter(company_id__in=company_search_ids)
        elif search_category == "2":
            products = products.filter(product_name__icontains=search_query)

    if filter_form.is_valid():
        price_min = filter_form.cleaned_data.get("price_min")
        price_max = filter_form.cleaned_data.get("price_max")
        company = filter_form.cleaned_data.get("company")
        nationality = filter_form.cleaned_data.get("nationality")

        if price_min is None:
            price_min = 0

        if price_max is None:
            price_max = 99999999999

        filtered_products = []
        for product in products:
            discounted_price = product.discounted_price
            if price_min <= discounted_price <= price_max:
                filtered_products.append(product.p_id)

        products = products.filter(p_id__in=filtered_products)
        if company:
            company_id = company.company_id
            products = products.filter(company_id=company_id)

        if nationality:
            company_ids = list(
                Company.objects.filter(nationality=nationality).values_list(
                    "company_id", flat=True
                )
            )
            products = products.filter(company_id__in=company_ids)
    # Pagination with 12 products per page
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page", 1)

    for product in products:
        product.check_expiry()

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page.
        products = paginator.page(paginator.num_pages)

    return render(
        request,
        "shop/product/list.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
            "filter_form": filter_form,
            "search_form": search_form,
            "cart_product_form": cart_form,
        },
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, p_id=id, slug=slug)
    product.check_expiry()
    cart_product_form = CartAddProductForm()
    return render(
        request,
        "shop/product/detail.html",
        {"product": product, "cart_product_form": cart_product_form},
    )

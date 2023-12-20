from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import CartWrapper
from .forms import CartAddProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.


@require_POST
def cart_add(request, p_id):
    user = request.user
    cart = CartWrapper(user)
    product = get_object_or_404(Product, p_id=p_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd["quantity"],
            override_quantity=cd["override"],
        )
    messages.success(request, f'{product.product_name} added to your cart successfully.')

    return redirect("shop:product_list")


@require_POST
def cart_remove(request, p_id):
    user = request.user
    cart = CartWrapper(user)
    product = get_object_or_404(Product, p_id=p_id)
    cart.remove(product)
    return redirect("cart:cart_detail")

@login_required
def cart_detail(request):
    user = request.user
    cart = CartWrapper(user)
    return render(request, "cart/detail.html", {"cart": cart})

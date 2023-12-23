from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_login
from shop.models import Product
from .cart import CartWrapper
from .forms import CartAddProductForm
from django.contrib import messages
from coupons.forms import CouponApplyForm
from django.contrib.auth.decorators import login_required


# Create your views here.


@require_login
@require_POST
def cart_add(request, p_id):
    user = request.user
    cart = CartWrapper(user)
    product = get_object_or_404(Product, p_id=p_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        if product.stock < cd["quantity"]:
            messages.error(
                request,
                f"Sorry, {product.product_name} stock is less than requested.",
                extra_tags="danger",
            )
            return redirect("shop:product_list")

        cart.add(
            product=product,
            quantity=cd["quantity"],
            override_quantity=cd["override"],
        )

        product.stock -= cd["quantity"]

        product.save()
    messages.success(
        request, f"{product.product_name} added to your cart successfully."
    )

    return redirect("shop:product_list")


@require_login
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
    coupon_apply_form = CouponApplyForm()
    return render(
        request,
        "cart/detail.html",
        {"cart": cart, "coupon_apply_form": coupon_apply_form},
    )

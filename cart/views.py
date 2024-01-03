from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .models import CartItem
from .cart import CartWrapper
from .forms import CartAddProductForm
from django.contrib import messages
from coupons.forms import CouponApplyForm
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
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
    return redirect("cart:cart_detail")


@login_required
@require_POST
def cart_remove(request, p_id):
    user = request.user
    cart = CartWrapper(user)
    product = get_object_or_404(Product, p_id=p_id)
    cart_items = CartItem.objects.filter(cart=cart.cart)
    for item in cart_items:
        if product == item.product:
            quantity = item.quantity
            cart.remove(product)

            # Add the removed quantity back to the product's stock
            product.stock += quantity
            product.save()

            messages.success(
                request, f"{product.product_name} removed from your cart successfully."
            )
            return redirect("cart:cart_detail")

    messages.error(
        request, f"{product.product_name} is not in your cart.", extra_tags="danger"
    )

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

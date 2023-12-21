from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm
from django.contrib import messages
from cart.models import Cart


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        try:
            coupon = Coupon.objects.get(
                code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True
            )
            cart = Cart.objects.get(user=request.user)
            cart.coupon = coupon
            cart.save()
            messages.error(request, "The coupon has been applied")
        except Coupon.DoesNotExist:
            messages.error(request, "This coupon does not exist")
    return redirect("cart:cart_detail")


@require_POST
def remove_coupon(request):
    cart = Cart.objects.get(user=request.user)
    if cart.coupon:
        cart.coupon = None
        cart.save()
        messages.error(request, "The coupon has been removed")
    else:
        messages.error(request, "No coupon to remove")
    return redirect("cart:cart_detail")

from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404,
    HttpResponseRedirect,
)
from orders.models import Order
from .tasks import payment_completed as payment_completed_task
from cart.cart import CartWrapper

# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get("order_id", None)
    order = get_object_or_404(Order, id=order_id)
    if order.order_processed:
        return redirect("payment:already_processed")

    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse("payment:completed"))
        cancel_url = request.build_absolute_uri(reverse("payment:canceled"))

        # Stripe checkout session data
        session_data = {
            "mode": "payment",
            "client_reference_id": order.id,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data["line_items"].append(
                {
                    "price_data": {
                        "unit_amount": int(item.price * Decimal("100")),
                        "currency": "EGP",
                        "product_data": {
                            "name": item.product.product_name,
                        },
                    },
                    "quantity": item.quantity,
                }
            )
        # Stripe coupon
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code, percent_off=order.discount, duration="once"
            )
            session_data["discounts"] = [{"coupon": stripe_coupon.id}]
        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)

        # redirect to Stripe payment form
        return redirect(session.url, code=303)

    else:
        return render(request, "payment/process.html", locals())


def cash_on_delivery(request):
    order_id = request.session.get("order_id", None)
    order = get_object_or_404(Order, id=order_id)
    if order.order_processed:
        return redirect("payment:already_processed")
    cart = CartWrapper(request.user)
    if order_id and not order.paid:
        order.paid = False
        order.order_processed = True
        order.save()
        payment_completed_task(order_id)
        cart.clear()
    return redirect("payment:process_successded_cod")


def payment_completed(request):
    order_id = request.session.get("order_id", None)
    order = get_object_or_404(Order, id=order_id)
    if order.order_processed:
        return redirect("payment:already_processed")
    cart = CartWrapper(request.user)
    print(order.paid)
    print(order.order_processed)
    if order_id and not order.paid:
        order.paid = True
        order.order_processed = True
        order.save()
        payment_completed_task(order_id)
        cart.clear()
        return redirect("payment:process_successded")
    return redirect("payment:canceled")


def process_successded(request):
    return render(request, "payment/completed.html")


def process_successded_cod(request):
    return render(request, "payment/completed_cod.html")


def payment_canceled(request):
    return render(request, "payment/canceled.html")


def already_processed(request):
    return render(request, "payment/already_processed.html")

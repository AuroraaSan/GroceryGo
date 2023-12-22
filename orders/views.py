from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from cart.cart import CartWrapper
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from account.models import Profile
from django.contrib.auth.models import User
import os
from django.contrib.auth.decorators import login_required
def order_create(request):
    cart = CartWrapper(request.user)

    if not cart:
        return redirect("cart:cart_detail")

    if request.method == "POST":
        form = OrderCreateForm(request.user, request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                 order.coupon = cart.coupon
                 order.discount = cart.coupon.discount
                 order.save()
            order.user = request.user
            order.address = form.cleaned_data["user_address"]
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm(request.user)

    return render(request, "orders/order/create.html", {"cart": cart, "form": form, "user": request.user})

        
def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/order/created.html", {"order": order})


@staff_member_required
def admin_order_pdf(request, order_id):
    # Assuming your views.py is in the 'orders' directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Navigate up one level to the project directory
    project_directory = os.path.dirname(current_directory)

    # Construct the path to the CSS file
    css_file_path = os.path.join(project_directory, "static", "css", "pdf.css")

    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/order/pdf.html", {"order": order})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order_{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(css_file_path)]
    )
    return response

@login_required
def user_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, "orders/order/user_orders.html", {"orders": orders, 'user':user})
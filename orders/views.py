from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import CartWrapper


def order_create(request):
    cart = CartWrapper(request.user)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # clear the cart
            cart.clear()

            return redirect("orders:order_created", order_id=order.id)
    else:
        form = OrderCreateForm()
    return render(request, "orders/order/create.html", {"cart": cart, "form": form})


def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/order/created.html", {"order": order})

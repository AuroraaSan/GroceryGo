from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import CartWrapper
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
#import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from account.models import Profile



def order_create(request):
    cart = CartWrapper(request.user)
    form = OrderCreateForm(user=request.user)
    # Check if the cart is empty
    if not cart:
        # Redirect the user to the cart view or display an error message
        return redirect("cart:cart_detail")
    
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    user_address = user_profile.address if not created else ""
    user_first_name = request.user.first_name
    user_last_name = request.user.last_name
    user_email = request.user.email


    if request.method == "POST":
        form = OrderCreateForm(request.user, request.POST)
        if form.is_valid():
            order = form.save()
            order.first_name = user_first_name
            order.last_name = user_last_name
            order.email = user_email
            order.save()
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
        form = OrderCreateForm(initial={'user_address': user_address, 'first_name': user_first_name, 'last_name': user_last_name, 'email': user_email, 'address': user_address}, user=request.user)

    return render(request, "orders/order/create.html", {"cart": cart, "form": form})

def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/order/created.html", {"order": order})

#@staff_member_required
#def admin_order_pdf(request, order_id):
#    order = get_object_or_404(Order, id=order_id)
#    html = render_to_string('orders/order/pdf.html',
#                            {'order': order})
#    response = HttpResponse(content_type='application/pdf')
#    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
#    weasyprint.HTML(string=html).write_pdf(response,
#        stylesheets=[weasyprint.CSS(
#            'D:\Semester7\Data Engineering\Project\GroceryGo\static_collected\css\pdf.css')])
#    return response
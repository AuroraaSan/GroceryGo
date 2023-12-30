from .cart import CartWrapper
from .models import CartItem


def cart(request):
    user_cart = CartWrapper(request.user)
    return {"cart": user_cart}
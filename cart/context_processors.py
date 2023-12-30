from .cart import CartWrapper


def cart(request):
    if request.user.is_authenticated:
        user_cart = CartWrapper(request.user)
        return {"cart": user_cart}
    else:
        return {"cart": None}

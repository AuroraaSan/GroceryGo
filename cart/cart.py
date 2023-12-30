from decimal import Decimal
from django.conf import settings
from shop.models import Product
from .models import Cart, CartItem
from .forms import CartAddProductForm
from django.db import models


class CartWrapper:
    def __init__(self, user):
        """
        Initialize the cart.
        """
        self.cart, created = Cart.objects.get_or_create(user=user)
        self.coupon = self.cart.coupon

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        cart_item, created = CartItem.objects.get_or_create(
            cart=self.cart, product=product
        )
        if override_quantity:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        CartItem.objects.filter(cart=self.cart, product=product).delete()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        cart_items = CartItem.objects.filter(cart=self.cart)
        for cart_item in cart_items:
            product = cart_item.product
            # Add the update_quantity_form to each item
            cart_item_dict = {
                "product": product,
                "quantity": cart_item.quantity,
                "price": product.price,
                "total_price": cart_item.total_price(),
                "update_quantity_form": CartAddProductForm(
                    initial={"quantity": cart_item.quantity, "override": True}
                ),
            }
            yield cart_item_dict

    def __len__(self):
        """
        Count all items in the cart.
        """
        return (
            CartItem.objects.filter(cart=self.cart).count()
            or 0
        )
    
    def get_total_price(self):
        return sum(
            cart_item.total_price()
            for cart_item in CartItem.objects.filter(cart=self.cart)
        )

    def clear(self):
        # remove cart from session
        CartItem.objects.filter(cart=self.cart).delete()

    @property
    def coupon_id(self):
        return self.coupon.id if self.coupon else None

    def get_discount(self):
        if self.coupon:
            return (Decimal(self.coupon.discount) / Decimal(100)) * Decimal(
                self.get_total_price()
            )
        return Decimal(0)

    def get_total_price_after_discount(self):
        return Decimal(self.get_total_price()) - Decimal(self.get_discount())

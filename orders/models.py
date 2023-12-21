from django.db import models
from shop.models import Product
from django.utils import timezone
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.contrib.auth.models import User
from account.models import Address


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    purchase_timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()
    def user_first_name(self):
        return self.user.first_name

    def user_last_name(self):
        return self.user.last_name

    def user_email(self):
        return self.user.email

    def user_address(self):
        # Assuming you have a related name 'profile' in User model
        return self.user.profile.address if hasattr(self.user, 'profile') else ''

    def user_postal_code(self):
        return self.user.profile.postal_code if hasattr(self.user, 'profile') else ''

    def user_city(self):
        return self.user.profile.city if hasattr(self.user, 'profile') else ''

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_product_info()

    def update_product_info(self):
        self.product.total_users_purchased += 1
        self.product.last_purchase_timestamp = timezone.now()
        last_24_hours_count = OrderItem.objects.filter(
            product=self.product,
            order__created__gte=timezone.now() - timezone.timedelta(hours=24),
        ).count()
        self.product.users_purchased_last_24_hours = last_24_hours_count
        self.product.save()

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

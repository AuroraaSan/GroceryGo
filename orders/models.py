from django.db import models
from shop.models import Product
from django.utils import timezone



class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
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

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


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
            order__created__gte=timezone.now() - timezone.timedelta(hours=24)
        ).count()
        self.product.users_purchased_last_24_hours = last_24_hours_count
        self.product.save()
    

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

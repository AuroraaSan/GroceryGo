from django.contrib import admin
from .models import Order, OrderItem
from account.models import Address, Profile
from django.utils.safestring import mark_safe
from django.urls import reverse


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


def order_pdf(obj):
    url = reverse("orders:admin_order_pdf", args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = "Invoice"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display = ['id', 'user', 'user_first_name', 'user_last_name', 'user_email',
    #                 'user_postal_code', 'user_city', 'paid',
    #               'created', 'updated', 'order_pdf']

    list_display = [
        "id",
        "user",
        "user_first_name",
        "user_last_name",
        "user_email",
        "user_address",
        "user_postal_code",
        "user_city",
        "user_country",
        "user_street",
        "paid",
        "order_processed",
        "created",
        "updated",
        "order_pdf",
    ]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]

    def user_first_name(self, obj):
        return obj.user.first_name

    def user_last_name(self, obj):
        return obj.user.last_name

    def user_email(self, obj):
        return obj.user.email

    def user_address(self, obj):
        return obj.address

    def user_street(self, obj):
        return obj.address.street

    def user_postal_code(self, obj):
        return obj.address.postal_code

    def user_city(self, obj):
        return obj.address.city

    def user_country(self, obj):
        return obj.address.country

    def order_pdf(self, obj):
        url = reverse("orders:admin_order_pdf", args=[obj.id])
        return mark_safe(f'<a href="{url}">PDF</a>')

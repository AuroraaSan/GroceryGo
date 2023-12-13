from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path("order/created/<int:order_id>/", views.order_created, name="order_created"),
]

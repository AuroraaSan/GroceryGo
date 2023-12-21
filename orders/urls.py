from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    # path('', views.user_orders, name="user_orders"),
    path("create/", views.order_create, name="order_create"),
    path("order/created/<int:order_id>/", views.order_created, name="order_created"),
    path('admin/order/<int:order_id>/pdf/',views.admin_order_pdf,name='admin_order_pdf'),
    path('user_orders/', views.user_orders, name='user_orders'),
]

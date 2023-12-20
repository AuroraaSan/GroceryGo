from django.urls import path
from . import views

app_name = "coupons"
urlpatterns = [
    path("apply/", views.coupon_apply, name="apply"),
    path("remove/", views.remove_coupon, name="remove"),
]

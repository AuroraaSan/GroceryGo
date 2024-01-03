from django.urls import path
from . import views
from . import webhooks

app_name = "payment"

urlpatterns = [
    path("process/", views.payment_process, name="process"),
    path("cod/", views.cash_on_delivery, name="cod"),
    path(
        "process_successded_cod/",
        views.process_successded_cod,
        name="process_successded_cod",
    ),
    path("already_processed/", views.already_processed, name="already_processed"),
    path(
        "process_successded/",
        views.process_successded,
        name="process_successded",
    ),
    path("completed/", views.payment_completed, name="completed"),
    path("canceled/", views.payment_canceled, name="canceled"),
    path("webhook/", webhooks.stripe_webhook, name="stripe-webhook"),
]

from django.urls import path
from .views.htmx import checkout_modal, checkout_submit

app_name = "orders"

urlpatterns = [
    path("", checkout_modal, name="checkout"),
    path("partials/checkout/submit/", checkout_submit, name="checkout_submit"),
]

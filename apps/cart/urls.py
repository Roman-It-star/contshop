from django.urls import path
from .views.htmx import cart_modal, cart_badge, cart_add, cart_set_qty, cart_remove

app_name = "cart"

urlpatterns = [
    path("partials/modal/", cart_modal, name="modal"),
    path("partials/badge/", cart_badge, name="badge"),
    path("add/<int:product_id>/", cart_add, name="add"),
    path("set/<int:product_id>/", cart_set_qty, name="set_qty"),
    path("remove/<int:product_id>/", cart_remove, name="remove"),
]

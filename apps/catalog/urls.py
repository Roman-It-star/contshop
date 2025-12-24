from django.urls import path
from .views.pages import catalog_page, product_detail
from .views.htmx import catalog_filter

app_name = "catalog"

urlpatterns = [
    path("", catalog_page, name="list"),

    path("partials/filter/", catalog_filter, name="filter"),
    path("partials/list/", catalog_filter, name="partial_list"),  # алиас

    path("<slug:slug>/", product_detail, name="detail"),
]

from django.urls import path
from .views.pages import catalog_page
from .views.htmx import catalog_list_partial

app_name = "catalog"

urlpatterns = [
    path("", catalog_page, name="page"),
    path("partials/list/", catalog_list_partial, name="partial_list"),
]

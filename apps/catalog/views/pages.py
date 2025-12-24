from django.shortcuts import render
from ..selectors import get_categories, get_products


def catalog_page(request):
    category = request.GET.get("category")
    context = {
        "categories": get_categories(),
        "products": get_products(category),
        "current_category": category,
    }
    return render(request, "catalog/pages/catalog.html", context)

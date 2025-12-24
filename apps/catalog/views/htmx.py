from django.shortcuts import render
from ..selectors import get_products


def catalog_list_partial(request):
    category = request.GET.get("category")
    context = {
        "products": get_products(category),
    }
    return render(request, "catalog/partials/product_list.html", context)

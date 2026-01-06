from django.shortcuts import get_object_or_404, render

from ..models import Product
from ..selectors import get_categories, get_products


def catalog_page(request):
    context = {
        "categories": get_categories(),
        "products": get_products("all"),
        "active_slug": "all",
    }
    return render(request, "catalog/pages/catalog.html", context)


def product_detail(request, slug: str):
    product = get_object_or_404(
        Product.objects.prefetch_related("categories", "images"),
        slug=slug
    )

    context = {
        "product": product,
        "categories": get_categories(),
    }
    return render(request, "catalog/pages/detail.html", context)

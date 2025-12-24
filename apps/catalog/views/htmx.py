from django.shortcuts import render
from django.views.decorators.http import require_GET

from ..selectors import get_categories, get_products


@require_GET
def catalog_filter(request):
    slug = request.GET.get("category", "all")

    context = {
        "categories": get_categories(),
        "products": get_products(slug),
        "active_slug": slug,
    }
    return render(request, "catalog/partials/catalog_block.html", context)

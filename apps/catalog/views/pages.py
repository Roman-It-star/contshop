from django.shortcuts import render, get_object_or_404
from ..selectors import get_categories, get_products
from ..models import Product

def catalog_page(request):
    category = request.GET.get("category")
    context = {
        "categories": get_categories(),
        "products": get_products(category),
        "current_category": category,
    }
    return render(request, "catalog/pages/catalog.html", context)


def product_detail(request, slug: str):
    product = get_object_or_404(Product.objects.prefetch_related("categories", "images"), slug=slug)
    return render(request, "catalog/pages/detail.html", {"product": product})
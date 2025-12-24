from django.db.models import QuerySet
from .models import Product, Category


def get_categories() -> QuerySet[Category]:
    return Category.objects.all()


def get_products(category_slug: str | None = None) -> QuerySet[Product]:
    qs = Product.objects.prefetch_related("categories", "images").all()
    if category_slug:
        qs = qs.filter(categories__slug=category_slug)
    return qs.distinct()

from django.db.models import QuerySet
from .models import Category, Product


def get_categories() -> QuerySet[Category]:
    return Category.objects.all().order_by("title")


def get_products(category_slug: str | None = None) -> QuerySet[Product]:
    qs = Product.objects.prefetch_related("categories").all().order_by("-id")

    if category_slug and category_slug != "all":
        qs = qs.filter(categories__slug=category_slug)

    return qs.distinct()


# если где-то уже использовал products_for_category — оставим совместимость
def products_for_category(category_slug: str | None) -> QuerySet[Product]:
    return get_products(category_slug)

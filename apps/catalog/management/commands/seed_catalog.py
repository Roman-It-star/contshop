import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from apps.catalog.models import Category, Product


def unique_slug(model, text: str) -> str:
    base = slugify(text)[:200] or "item"
    slug = base
    i = 2
    while model.objects.filter(slug=slug).exists():
        slug = f"{base}-{i}"
        i += 1
    return slug


class Command(BaseCommand):
    help = "Создает тестовые данные для каталога (категории + товары)."

    def add_arguments(self, parser):
        parser.add_argument("--categories", type=int, default=6)
        parser.add_argument("--products", type=int, default=30)
        parser.add_argument("--clear", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        categories_count = options["categories"]
        products_count = options["products"]
        clear = options["clear"]

        if clear:
            Product.objects.all().delete()
            Category.objects.all().delete()

        titles = [
            "20' Standard",
            "20' High-Cube",
            "40' Standard",
            "40' High-Cube",
            "Рефрижераторные",
            "Под склад / бытовку",
        ][: max(1, categories_count)]

        categories = []
        for t in titles:
            slug = unique_slug(Category, t)
            c, _ = Category.objects.get_or_create(slug=slug, defaults={"title": t})
            categories.append(c)

        for i in range(products_count):
            size = random.choice([Product.SIZE_20, Product.SIZE_40])
            ctype = random.choice([Product.TYPE_STD, Product.TYPE_HC])
            cond = random.choice([Product.CONDITION_NEW, Product.CONDITION_USED])

            title = f"Контейнер {size}' {('High-Cube' if ctype == Product.TYPE_HC else 'Standard')} ({'новый' if cond == Product.CONDITION_NEW else 'б/у'}) #{i+1}"
            slug = unique_slug(Product, title)

            base_price = Decimal("180000") if size == Product.SIZE_20 else Decimal("260000")
            if ctype == Product.TYPE_HC:
                base_price += Decimal("25000")
            if cond == Product.CONDITION_USED:
                base_price -= Decimal("45000")

            price_sale = max(Decimal("90000"), base_price + Decimal(str(random.randint(-10000, 20000))))

            product = Product.objects.create(
                title=title,
                slug=slug,
                description="Тестовый контейнер для демонстрации каталога. Условия уточняются при заявке.",
                size=size,
                container_type=ctype,
                condition=cond,
                is_for_sale=True,
                is_for_rent=random.choice([True, False]),
                price_sale=price_sale,
                rent_terms="от 12000 ₽/мес, залог 1 мес.",
                availability=random.choice([Product.AVAILABILITY_IN_STOCK, Product.AVAILABILITY_ON_ORDER, Product.AVAILABILITY_OUT]),
            )
            product.categories.set(random.sample(categories, k=random.randint(1, min(3, len(categories)))))

        self.stdout.write(self.style.SUCCESS(f"Готово. Категорий: {Category.objects.count()}, товаров: {Product.objects.count()}"))

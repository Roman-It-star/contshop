from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug= slugify(self.title)
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Product(models.Model):
    AVAILABILITY_IN_STOCK = "in_stock"
    AVAILABILITY_ON_ORDER = "on_order"
    AVAILABILITY_OUT = "out"

    AVAILABILITY_CHOICES = [
        (AVAILABILITY_IN_STOCK, "В наличии"),
        (AVAILABILITY_ON_ORDER, "Под заказ"),
        (AVAILABILITY_OUT, "Нет"),
    ]

    CONDITION_NEW = "new"
    CONDITION_USED = "used"

    CONDITION_CHOICES = [
        (CONDITION_NEW, "Новый"),
        (CONDITION_USED, "Б/у"),
    ]

    SIZE_20 = "20"
    SIZE_40 = "40"

    SIZE_CHOICES = [
        (SIZE_20, "20 футов"),
        (SIZE_40, "40 футов"),
    ]

    TYPE_STD = "standard"
    TYPE_HC = "high_cube"

    TYPE_CHOICES = [
        (TYPE_STD, "Standard"),
        (TYPE_HC, "High-Cube"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)

    categories = models.ManyToManyField(Category, related_name="products", blank=True)

    size = models.CharField(max_length=2, choices=SIZE_CHOICES, blank=True)
    container_type = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, blank=True)

    is_for_sale = models.BooleanField(default=True)
    is_for_rent = models.BooleanField(default=False)

    price_sale = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rent_terms = models.CharField(max_length=200, blank=True)

    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default=AVAILABILITY_IN_STOCK)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товаров"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product_id}#{self.id}"

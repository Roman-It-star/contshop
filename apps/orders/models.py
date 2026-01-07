from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
<<<<<<< HEAD

from apps.catalog.models import Product
=======
from apps.catalog.models import Product
from apps.customers.models import Customer
>>>>>>> feature/from-archive


class Order(models.Model):
    TG_STATUS_PENDING = "pending"
    TG_STATUS_SENT = "sent"
    TG_STATUS_FAILED = "failed"

    TG_STATUS_CHOICES = [
        (TG_STATUS_PENDING, "Ожидает отправки"),
        (TG_STATUS_SENT, "Отправлено"),
        (TG_STATUS_FAILED, "Ошибка отправки"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Телефон", max_length=32, blank=True)
    email = models.EmailField("Email", blank=True)
    comment = models.TextField("Комментарий", blank=True)

<<<<<<< HEAD
=======
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Клиент'
    )
    
>>>>>>> feature/from-archive
    total = models.DecimalField(
        "Итого",
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    tg_status = models.CharField(
        "Статус отправки в Telegram",
        max_length=16,
        choices=TG_STATUS_CHOICES,
        default=TG_STATUS_PENDING,
    )
    attempts_count = models.PositiveIntegerField("Попыток отправки", default=0)
    last_attempt_at = models.DateTimeField("Последняя попытка", null=True, blank=True)
    last_error_short = models.CharField("Последняя ошибка (кратко)", max_length=255, blank=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Заявка #{self.id} от {self.created_at:%Y-%m-%d %H:%M}"

    @property
    def contact(self) -> str:
        return self.phone or self.email or ""


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")

    title = models.CharField("Название (на момент заявки)", max_length=200)
    price = models.DecimalField("Цена (на момент заявки)", max_digits=12, decimal_places=2, default=Decimal("0.00"))
    qty = models.PositiveIntegerField("Количество", default=1)

    line_total = models.DecimalField(
        "Сумма",
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    class Meta:
        verbose_name = "Позиция заявки"
        verbose_name_plural = "Позиции заявки"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.title} × {self.qty}"

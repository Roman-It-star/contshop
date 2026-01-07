from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Customer(AbstractUser):
    phone = models.CharField("Телефон", max_length=20, blank=True)
    company = models.CharField("Компания", max_length=100, blank=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        
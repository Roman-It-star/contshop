from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("title", "price", "qty", "line_total")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "name", "phone", "email", "total", "tg_status", "attempts_count")
    list_filter = ("tg_status", "created_at")
    search_fields = ("name", "phone", "email")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at", "total", "tg_status", "attempts_count", "last_attempt_at", "last_error_short")

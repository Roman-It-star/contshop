from decimal import Decimal
from django.db import transaction
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from apps.orders.models import Order, OrderItem
from apps.cart import services as cart_services


@require_GET
def checkout_modal(request):
    lines = cart_services.get_lines(request.session)
    total = cart_services.get_total(request.session)

    return render(
        request,
        "orders/partials/checkout_form.html",
        {
            "errors": {},
            "name": "",
            "phone": "",
            "email": "",
            "comment": "",
            "lines": lines,
            "total": total,
            "count": cart_services.count_items(request.session),
        },
    )


@require_POST
def checkout_submit(request):
    name = (request.POST.get("name") or "").strip()
    phone = (request.POST.get("phone") or "").strip()
    email = (request.POST.get("email") or "").strip()
    comment = (request.POST.get("comment") or "").strip()

    lines = cart_services.get_lines(request.session)

    errors = {}
    if not name:
        errors["name"] = "Укажите имя"
    if not phone and not email:
        errors["contact"] = "Укажите телефон или email"
    if not lines:
        errors["cart"] = "Корзина пуста"

    if errors:
        return render(
            request,
            "orders/partials/checkout_form.html",
            {
                "errors": errors,
                "name": name,
                "phone": phone,
                "email": email,
                "comment": comment,
                "lines": lines,
                "total": cart_services.get_total(request.session),
                "count": cart_services.count_items(request.session),
            },
            status=400,
        )

    with transaction.atomic():
        order = Order.objects.create(
            name=name,
            phone=phone,
            email=email,
            comment=comment,
            total=Decimal("0.00"),
        )

        items_total = Decimal("0.00")

        for line in lines:
            product = line.product
            qty = int(line.qty)

            price = product.price_sale or Decimal("0.00")
            line_total = (price * qty).quantize(Decimal("0.01"))
            items_total += line_total

            OrderItem.objects.create(
                order=order,
                product=product,
                title=product.title,
                price=price,
                qty=qty,
                line_total=line_total,
            )

        order.total = items_total
        order.save(update_fields=["total"])

        clear_fn = getattr(cart_services, "clear", None)
        if callable(clear_fn):
            clear_fn(request.session)
        else:
            request.session.pop("cart", None)
            request.session.modified = True

    return render(
        request,
        "orders/partials/checkout_success.html",
        {"order": order, "count": cart_services.count_items(request.session)},
    )

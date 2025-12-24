from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from ..services import add, set_qty, remove, get_lines, get_total, count_items


def _cart_context(request):
    return {
        "lines": get_lines(request.session),
        "total": get_total(request.session),
        "count": count_items(request.session),
    }


@require_GET
def cart_modal(request):
    return render(request, "cart/partials/modal_body.html", _cart_context(request))


@require_GET
def cart_badge(request):
    return render(request, "cart/partials/badge.html", {"count": count_items(request.session)})


@require_POST
def cart_add(request, product_id: int):
    add(request.session, product_id, qty=1)

    context = {
        "lines": get_lines(request.session),
        "total": get_total(request.session),
        "count": count_items(request.session),
        "oob": True,
    }
    return render(request, "cart/partials/oob_modal_update.html", context)


@require_POST
def cart_set_qty(request, product_id: int):
    qty = int(request.POST.get("qty", "1"))
    set_qty(request.session, product_id, qty)
    return render(request, "cart/partials/modal_body.html", _cart_context(request))


@require_POST
def cart_remove(request, product_id: int):
    remove(request.session, product_id)
    return render(request, "cart/partials/modal_body.html", _cart_context(request))

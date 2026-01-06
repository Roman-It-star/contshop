from decimal import Decimal
from dataclasses import dataclass
from typing import Any

from apps.catalog.models import Product


SESSION_KEY = "cart"


@dataclass(frozen=True)
class CartLine:
    product: Product
    qty: int
    line_total: Decimal


def _get_raw(session: Any) -> dict[str, int]:
    return session.get(SESSION_KEY, {})


def _save_raw(session: Any, raw: dict[str, int]) -> None:
    session[SESSION_KEY] = raw
    session.modified = True


def add(session: Any, product_id: int, qty: int = 1) -> None:
    raw = _get_raw(session)
    key = str(product_id)
    raw[key] = int(raw.get(key, 0)) + int(qty)
    if raw[key] <= 0:
        raw.pop(key, None)
    _save_raw(session, raw)


def set_qty(session: Any, product_id: int, qty: int) -> None:
    raw = _get_raw(session)
    key = str(product_id)
    qty = int(qty)
    if qty <= 0:
        raw.pop(key, None)
    else:
        raw[key] = qty
    _save_raw(session, raw)


def remove(session: Any, product_id: int) -> None:
    raw = _get_raw(session)
    raw.pop(str(product_id), None)
    _save_raw(session, raw)


def clear(session: Any) -> None:
    _save_raw(session, {})


def count_items(session: Any) -> int:
    raw = _get_raw(session)
    return sum(int(v) for v in raw.values())


def get_lines(session: Any) -> list[CartLine]:
    raw = _get_raw(session)
    if not raw:
        return []

    ids = [int(k) for k in raw.keys()]
    products = {p.id: p for p in Product.objects.filter(id__in=ids)}
    lines: list[CartLine] = []

    for k, v in raw.items():
        pid = int(k)
        product = products.get(pid)
        if not product:
            continue
        qty = int(v)
        price = product.price_sale or Decimal("0")
        lines.append(CartLine(product=product, qty=qty, line_total=price * qty))

    return lines


def get_total(session: Any) -> Decimal:
    return sum((l.line_total for l in get_lines(session)), Decimal("0"))

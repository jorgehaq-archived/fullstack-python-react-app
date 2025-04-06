import strawberry
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from app.domain.orders.entities import Order as OrderEntity, OrderItem as OrderItemEntity

@strawberry.input
class OrderItemInput:
    product_id: str
    quantity: int
    price: float

@strawberry.type
class OrderItem:
    id: str
    product_id: str
    quantity: int
    price: float
    
    @classmethod
    def from_domain(cls, item: OrderItemEntity) -> 'OrderItem':
        return cls(
            id=str(item.id),
            product_id=str(item.product_id),
            quantity=item.quantity,
            price=item.price
        )

@strawberry.type
class Order:
    id: str
    user_id: str
    items: List[OrderItem]
    subtotal: float
    taxes: float
    total: float
    status: str
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, order: OrderEntity) -> 'Order':
        return cls(
            id=str(order.id),
            user_id=str(order.user_id),
            items=[OrderItem.from_domain(item) for item in order.items],
            subtotal=order.subtotal,
            taxes=order.taxes,
            total=order.total,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at
        )
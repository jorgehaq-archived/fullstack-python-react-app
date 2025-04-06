# api/graphql/order_mutations.py

import strawberry
from uuid import UUID
from typing import List

from app.domain.orders.services import OrderService
from app.domain.orders.entities import Order, OrderItem
from .types import OrderType, OrderItemInput

@strawberry.type
class OrderMutations:
    @strawberry.mutation
    async def create_order(
        self, 
        user_id: str, 
        items: List[OrderItemInput],
        order_service: OrderService
    ) -> OrderType:
        # Convertir de tipo GraphQL a entidad de dominio
        domain_items = [
            OrderItem(
                product_id=UUID(item.product_id),
                quantity=item.quantity,
                price=item.price
            )
            for item in items
        ]
        
        # Llamar al servicio de dominio
        order = await order_service.create_order(
            user_id=UUID(user_id),
            items=domain_items
        )
        
        # Convertir el resultado a tipo GraphQL
        return OrderType.from_domain(order)
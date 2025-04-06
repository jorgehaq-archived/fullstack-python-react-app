import strawberry
from uuid import UUID
from typing import List

from app.domain.orders.entities import OrderItem
from app.domain.orders.services import OrderService
from backend.app.api.graphql.types.orders.order_types import Order as OrderType, OrderItemInput
from app.config.dependencies import get_order_service

@strawberry.type
class OrderMutations:
    @strawberry.mutation
    async def create_order(
        self, 
        user_id: str, 
        items: List[OrderItemInput],
        order_service: OrderService = Depends(get_order_service)
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
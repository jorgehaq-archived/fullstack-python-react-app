# services.py dentro del módulo orders

from typing import List
from uuid import UUID
from datetime import datetime

from .entities import Order, OrderItem
from .interfaces import OrderRepository, OrderStatusManager, OrderCalculator
from ..notifications.interfaces import NotificationService
from ..inventory.interfaces import InventoryService

class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        order_status_manager: OrderStatusManager,
        order_calculator: OrderCalculator,
        notification_service: NotificationService,
        inventory_service: InventoryService
    ):
        self.order_repository = order_repository
        self.order_status_manager = order_status_manager
        self.order_calculator = order_calculator
        self.notification_service = notification_service
        self.inventory_service = inventory_service

    async def create_order(self, user_id: UUID, items: List[OrderItem]) -> Order:
        # Verificar disponibilidad en inventario
        for item in items:
            is_available = await self.inventory_service.check_availability(item.product_id, item.quantity)
            if not is_available:
                raise ValueError(f"Product {item.product_id} not available in the requested quantity")

        # Calcular valores
        subtotal = self.order_calculator.calculate_subtotal(items)
        taxes = self.order_calculator.calculate_taxes(subtotal)
        total = self.order_calculator.calculate_total(subtotal, taxes)

        # Crear orden
        new_order = Order(
            user_id=user_id,
            items=items,
            subtotal=subtotal,
            taxes=taxes,
            total=total,
            status="pending",
            created_at=datetime.now()
        )
        
        created_order = await self.order_repository.create(new_order)
        
        # Actualizar inventario
        for item in items:
            await self.inventory_service.reduce_stock(item.product_id, item.quantity)
            
        # Enviar notificación
        await self.notification_service.send_notification(
            user_id, 
            "order_created", 
            {"order_id": str(created_order.id), "total": total}
        )
        
        return created_order
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.orders.interfaces import OrderStatusManager, OrderCalculator
from app.domain.orders.entities import Order, OrderItem

class DefaultOrderStatusManager(OrderStatusManager):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    async def change_status(self, order_id: UUID, new_status: str, reason: str = None) -> Order:
        # Implementación de cambio de estado
        # Verifica reglas de transición de estado
        # Actualiza la base de datos
        # Retorna orden actualizada
        pass
        
    async def get_status_history(self, order_id: UUID) -> List[dict]:
        # Implementación para obtener historial de estados
        pass
        
class StandardOrderCalculator(OrderCalculator):
    def calculate_subtotal(self, items: List[OrderItem]) -> float:
        return sum(item.price * item.quantity for item in items)
        
    def calculate_taxes(self, subtotal: float, tax_rate: float = 0.16) -> float:
        return subtotal * tax_rate
        
    def calculate_total(self, subtotal: float, taxes: float, discount: float = 0) -> float:
        return subtotal + taxes - discount
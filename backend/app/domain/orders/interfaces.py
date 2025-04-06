# interfaces.py dentro del módulo orders
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from .entities import Order, OrderItem

class OrderRepository(ABC):
    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    async def create(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def update(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def delete(self, order_id: UUID) -> bool:
        pass

    @abstractmethod
    async def list_by_user(self, user_id: UUID, limit: int = 100, offset: int = 0) -> List[Order]:
        pass

class OrderStatusManager(ABC):
    @abstractmethod
    async def change_status(self, order_id: UUID, new_status: str) -> Order:
        pass

    @abstractmethod
    async def get_status_history(self, order_id: UUID) -> List[dict]:
        pass

class OrderCalculator(ABC):
    @abstractmethod
    def calculate_subtotal(self, items: List[OrderItem]) -> float:
        pass

    @abstractmethod
    def calculate_taxes(self, subtotal: float) -> float:
        pass

    @abstractmethod
    def calculate_total(self, subtotal: float, taxes: float, discount: float = 0) -> float:
        pass
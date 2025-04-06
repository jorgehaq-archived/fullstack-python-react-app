class OrderRepository(ABC):
    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        """Recupera una orden por su ID"""
        pass

    @abstractmethod
    async def list_by_user(self, user_id: UUID, limit: int = 100, offset: int = 0) -> List[Order]:
        """Lista órdenes de un usuario específico"""
        pass

    @abstractmethod
    async def create(self, order: Order) -> Order:
        """Crea una nueva orden"""
        pass

    @abstractmethod
    async def update(self, order: Order) -> Order:
        """Actualiza una orden existente"""
        pass

    @abstractmethod
    async def delete(self, order_id: UUID) -> bool:
        """Elimina una orden por su ID"""
        pass



class OrderStatusManager(ABC):
    @abstractmethod
    async def change_status(self, order_id: UUID, new_status: str, reason: str = None) -> Order:
        """Cambia el estado de una orden"""
        pass

    @abstractmethod
    async def get_status_history(self, order_id: UUID) -> List[dict]:
        """Obtiene el historial de estados de una orden"""
        pass


    

class OrderCalculator(ABC):
    @abstractmethod
    def calculate_subtotal(self, items: List[OrderItem]) -> float:
        """Calcula el subtotal de una orden"""
        pass

    @abstractmethod
    def calculate_taxes(self, subtotal: float, tax_rate: float = 0.16) -> float:
        """Calcula los impuestos de una orden"""
        pass

    @abstractmethod
    def calculate_total(self, subtotal: float, taxes: float, discount: float = 0) -> float:
        """Calcula el total de una orden"""
        pass
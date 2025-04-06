    # infrastructure/repositories.py
    
    from typing import List, Optional
    from uuid import UUID
    from sqlalchemy.orm import Session
    
    from app.domain.orders.entities import Order, OrderItem
    from app.domain.orders.interfaces import OrderRepository
    from app.db.models import OrderModel, OrderItemModel
    
    class SQLAlchemyOrderRepository(OrderRepository):
        def __init__(self, db_session: Session):
            self.db_session = db_session
            
        async def get_by_id(self, order_id: UUID) -> Optional[Order]:
            db_order = self.db_session.query(OrderModel).filter(OrderModel.id == order_id).first()
            if not db_order:
                return None
            
            # Convertir de modelo DB a entidad de dominio
            return self._map_to_domain(db_order)
        
        # Implementación de otros métodos...
        
        def _map_to_domain(self, db_order: OrderModel) -> Order:
            items = [
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price
                ) 
                for item in db_order.items
            ]
            
            return Order(
                id=db_order.id,
                user_id=db_order.user_id,
                items=items,
                subtotal=db_order.subtotal,
                taxes=db_order.taxes,
                total=db_order.total,
                status=db_order.status,
                created_at=db_order.created_at
            )
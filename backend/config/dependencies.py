    # config/dependencies.py
    
    from fastapi import Depends
    from sqlalchemy.orm import Session
    
    from app.db.session import get_db
    from app.domain.orders.interfaces import OrderRepository, OrderStatusManager, OrderCalculator
    from app.domain.orders.services import OrderService
    from app.infrastructure.repositories import SQLAlchemyOrderRepository
    from app.infrastructure.services import DefaultOrderStatusManager, StandardOrderCalculator
    from app.domain.notifications.interfaces import NotificationService
    from app.infrastructure.notifications import EmailNotificationService
    from app.domain.inventory.interfaces import InventoryService
    from app.infrastructure.inventory import PostgresInventoryService
    
    def get_order_repository(db: Session = Depends(get_db)) -> OrderRepository:
        return SQLAlchemyOrderRepository(db)
    
    def get_order_status_manager(db: Session = Depends(get_db)) -> OrderStatusManager:
        return DefaultOrderStatusManager(db)
    
    def get_order_calculator() -> OrderCalculator:
        return StandardOrderCalculator()
    
    def get_notification_service() -> NotificationService:
        return EmailNotificationService()
    
    def get_inventory_service(db: Session = Depends(get_db)) -> InventoryService:
        return PostgresInventoryService(db)
    
    def get_order_service(
        repository: OrderRepository = Depends(get_order_repository),
        status_manager: OrderStatusManager = Depends(get_order_status_manager),
        calculator: OrderCalculator = Depends(get_order_calculator),
        notification_service: NotificationService = Depends(get_notification_service),
        inventory_service: InventoryService = Depends(get_inventory_service)
    ) -> OrderService:
        return OrderService(
            repository, 
            status_manager, 
            calculator, 
            notification_service, 
            inventory_service
        )
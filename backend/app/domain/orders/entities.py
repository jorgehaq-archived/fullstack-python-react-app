class Order:
    def __init__(
        self,
        id: UUID = None,
        user_id: UUID = None,
        items: List[OrderItem] = None,
        subtotal: float = 0.0,
        taxes: float = 0.0,
        total: float = 0.0,
        status: str = "pending",
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        self.id = id or uuid.uuid4()
        self.user_id = user_id
        self.items = items or []
        self.subtotal = subtotal
        self.taxes = taxes
        self.total = total
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or self.created_at


class OrderItem:
    def __init__(
        self,
        id: UUID = None,
        order_id: UUID = None,
        product_id: UUID = None,
        quantity: int = 1,
        price: float = 0.0
    ):
        self.id = id or uuid.uuid4()
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
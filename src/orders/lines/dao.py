from src.dao import BaseDAO
from src.orders.lines.models import OrderLine


class OrderLineDAO(BaseDAO):
    model = OrderLine

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from database.db_init import db
from .user_model import User
from .product_model import Product
from .order_model import Order
from .order_item_model import OrderItem

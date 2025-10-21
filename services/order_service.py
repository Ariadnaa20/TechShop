"""
Lògica de negoci relacionada amb les comandes.
"""
from models.models import db, Order, OrderItem, Product

class OrderService:

    @staticmethod
    def create_order(cart: dict, user_id: int):
        """
        Crea una comanda amb les línies del carretó.
        Args:
            cart (dict): product_id -> quantity
            user_id (int): id de l'usuari
        Returns:
            Order: instància de la comanda creada
        Raises:
            ValueError: si el carretó està buit o stock insuficient
        """
        if not cart:
            raise ValueError("El carretó està buit.")

        total = 0
        order_items = []

        for product_id, quantity in cart.items():
            product = Product.query.get(product_id)
            if not product:
                raise ValueError(f"Producte {product_id} no existeix.")
            if quantity > product.stock:
                raise ValueError(f"No hi ha prou stock per {product.name}.")

            total += float(product.price) * quantity
            order_items.append(OrderItem(product_id=product.id, quantity=quantity))
            product.stock -= quantity  # actualitzar stock

        # Crear comanda
        order = Order(total=total, user_id=user_id)
        db.session.add(order)
        db.session.commit()  # necessitem l'ID de la comanda per afegir OrderItems

        for item in order_items:
            item.order_id = order.id
            db.session.add(item)

        db.session.commit()
        return order

"""
Lògica de negoci relacionada amb els productes.
"""
from models import db
from models import Product, db


class ProductService:
    @staticmethod
    def get_all_products():
        """
        Retorna tots els productes disponibles.
        Returns:
            list[Product]: llista de productes
        """
        return Product.query.all()

    @staticmethod
    def get_product_by_id(product_id: int):
        """
        Cerca un producte pel seu ID.
        Args:
            product_id (int): identificador del producte
        Returns:
            Product | None: producte trobat o None
        """
        return Product.query.get(product_id)

    @staticmethod
    def update_stock(product_id: int, quantity: int):
        """
        Resta unitats de stock després d'una compra.
        Args:
            product_id (int): id del producte
            quantity (int): unitats a restar
        Raises:
            ValueError: si no hi ha prou stock
        """
        product = Product.query.get(product_id)
        if not product:
            raise ValueError("Producte no trobat.")
        if product.stock < quantity:
            raise ValueError(f"No hi ha prou stock per a {product.name}. Disponible: {product.stock}")
        
        product.stock -= quantity
        db.session.commit()
        return product

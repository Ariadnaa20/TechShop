from models import Product


class CartService:
    MAX_QUANTITY_PER_PRODUCT = 5

    @staticmethod
    def add_to_cart(cart: dict, product: Product, quantity: int):
        if quantity < 1:
            raise ValueError("La quantitat ha de ser un enter positiu.")
        current_qty = cart.get(product.id, 0)
        if current_qty + quantity > CartService.MAX_QUANTITY_PER_PRODUCT:
            raise ValueError(f"No es poden afegir més de {CartService.MAX_QUANTITY_PER_PRODUCT} unitats per producte.")
        cart[product.id] = current_qty + quantity
        return cart

    @staticmethod
    def remove_from_cart(cart: dict, product_id: int):
        if product_id in cart:
            del cart[product_id]
        return cart

    @staticmethod
    def validate_stock(product: Product, quantity: int):
        if quantity > product.stock:
            raise ValueError(f"No hi ha prou unitats disponibles. Stock actual: {product.stock}")

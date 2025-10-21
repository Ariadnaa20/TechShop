from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.models import Product, db
from services.cart_service import CartService

bp = Blueprint('routes', __name__)

# RUTA HOME
@bp.route('/')
def home():
    return redirect(url_for('routes.show_products'))

# MOSTRAR PRODUCTES
@bp.route('/products')
def show_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

# CARRETÓ
@bp.route('/cart')
def show_cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            subtotal = float(product.price) * quantity
            total += subtotal
            cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render_template('cart.html', cart=cart_items, total=total)

# AFEGIR AL CARRETÓ
@bp.route('/add_to_cart/<int:product_id>/<int:quantity>')
def add_to_cart(product_id, quantity):
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', {})
    try:
        CartService.validate_stock(product, quantity)
        CartService.add_to_cart(cart, product, quantity)
        session['cart'] = cart
        flash(f"S'ha afegit {quantity} unitats de {product.name}", 'success')
    except ValueError as e:
        flash(str(e), 'error')
    return redirect(url_for('routes.show_products'))

# ELIMINAR DEL CARRETÓ
@bp.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    CartService.remove_from_cart(cart, product_id)
    session['cart'] = cart
    flash("Producte eliminat del carretó", 'success')
    return redirect(url_for('routes.show_cart'))

# CHECKOUT
@bp.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash("El carretó està buit", 'error')
        return redirect(url_for('routes.show_products'))

    # Aquí podries afegir la lògica per crear la comanda (Order i OrderItem)
    # i restar el stock dels productes.

    flash("Compra finalitzada! (funcionalitat demo)", 'success')
    session['cart'] = {}
    return redirect(url_for('routes.show_products'))

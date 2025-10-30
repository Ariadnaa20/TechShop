from werkzeug.security import generate_password_hash
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models import db, Product, User, Order, OrderItem
from services.cart_service import CartService
from datetime import datetime

bp = Blueprint('routes', __name__)

# 🏠 HOME → Redirigeix al formulari de checkout
@bp.route('/')
def home():
    return redirect(url_for('routes.checkout'))


# 🧾 CHECKOUT → Formulari inicial amb validacions

@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        address = request.form.get('address')  # pots deixar-ho encara que no s’emmagatzemi

        if not username or not password or not email:
            flash("Tots els camps són obligatoris ⚠️", "error")
            return render_template('checkout.html')

        # 🔹 Comprovar si l’usuari ja existeix
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            session['user_id'] = existing_user.id
            flash(f"Benvinguda de nou, {username}! 👋", "success")
        else:
            # 🔹 Crear nou usuari amb contrasenya xifrada
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username,
                password_hash=hashed_password,
                email=email
            )
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            flash(f"Benvinguda, {username}! Compte creat correctament 🛍️", "success")

        return redirect(url_for('routes.show_products'))

    return render_template('checkout.html')




# 🛒 MOSTRAR PRODUCTES
@bp.route('/products')
def show_products():
    if 'user_id' not in session:
        flash("Has d'omplir el formulari abans de continuar ⚠️", "error")
        return redirect(url_for('routes.checkout'))

    products = Product.query.all()
    user = User.query.get(session.get('user_id'))
    return render_template('products.html', products=products, user=user)


# 🛍️ MOSTRAR CARRETÓ
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
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
    return render_template('cart.html', cart=cart_items, total=total)


# 💳 FINALITZAR COMPRA
@bp.route('/finish_checkout')
def finish_checkout():
    if 'user_id' not in session:
        flash("Has d'omplir el formulari abans de continuar ⚠️", "error")
        return redirect(url_for('routes.checkout'))

    cart = session.get('cart', {})
    if not cart:
        flash("El carretó està buit 🛒", 'error')
        return redirect(url_for('routes.show_products'))

    user_id = session['user_id']
    total = 0
    order_items = []

    # 🔹 Calcular total i preparar línies de comanda
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            subtotal = float(product.price) * quantity
            total += subtotal
            order_items.append((product, quantity, subtotal))

    # 🔹 Crear comanda
    new_order = Order(user_id=user_id, date=datetime.now(), total=total)
    db.session.add(new_order)
    db.session.commit()  # Guardem per obtenir ID

    # 🔹 Crear cada línia (OrderItem)
    for product, quantity, subtotal in order_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=quantity,
            price=product.price
        )
        db.session.add(order_item)

        # Reduir stock
        product.stock -= quantity

    db.session.commit()

    # 🔹 Netejar carretó
    session['cart'] = {}
    flash("Compra finalitzada correctament! ✅", 'success')

    return render_template('order_succes.html', total=total)
    

# ➕ AFEGIR PRODUCTE AL CARRETÓ
@bp.route('/add_to_cart/<int:product_id>/<int:quantity>', methods=['GET', 'POST'])
def add_to_cart(product_id, quantity):
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', {})

    try:
        CartService.validate_stock(product, quantity)
        CartService.add_to_cart(cart, product, quantity)
        session['cart'] = cart
        flash(f"S'han afegit {quantity} unitats de {product.name} al carretó ✅", 'success')
    except ValueError as e:
        flash(str(e), 'error')

    return redirect(url_for('routes.show_products'))


# 🗑️ ELIMINAR PRODUCTE DEL CARRETÓ
@bp.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    CartService.remove_from_cart(cart, product_id)
    session['cart'] = cart
    flash("Producte eliminat del carretó 🗑️", 'success')
    return redirect(url_for('routes.show_cart'))

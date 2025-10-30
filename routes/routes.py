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
        address = request.form.get('address')  # per ara no s'emmagatzema

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
            new_user = User(username=username, password_hash=hashed_password, email=email)
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

    # 🔹 Convertim claus de string a int per buscar productes correctament
    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
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

    print("🧩 Dades de sessió actual:", session)
    print("🛍️ Carret actual:", cart)

    user_id = session['user_id']
    total = 0
    order_items = []

    # 🔹 Calcular total i preparar items
    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = Product.query.get(product_id)
        if product:
            subtotal = float(product.price) * quantity
            total += subtotal
            order_items.append((product, quantity, subtotal))

    # 🔹 Crear ordre
    new_order = Order(user_id=user_id, total=total, created_at=datetime.now())
    db.session.add(new_order)
    db.session.commit()  # necessari per obtenir ID

    # 🔹 Crear línies de comanda
    for product, quantity, subtotal in order_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=quantity
        )
        db.session.add(order_item)
        product.stock -= quantity

    db.session.commit()

    # 🔹 Netejar carretó
    session['cart'] = {}
    session.modified = True

    flash("Compra finalitzada correctament! ✅", 'success')
    return render_template('order_succes.html', total=total)


# ➕ AFEGIR PRODUCTE AL CARRETÓ
@bp.route('/add_to_cart/<int:product_id>/<int:quantity>', methods=['GET', 'POST'])
def add_to_cart(product_id, quantity):
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', {})

    # 🔹 Convertim la clau a string per evitar errors de serialització
    product_key = str(product_id)

    try:
        CartService.validate_stock(product, quantity)
        cart[product_key] = cart.get(product_key, 0) + quantity
        session['cart'] = cart
        session.modified = True
        flash(f"S'han afegit {quantity} unitats de {product.name} al carretó ✅", 'success')
    except ValueError as e:
        flash(str(e), 'error')

    return redirect(url_for('routes.show_products'))


# 🗑️ ELIMINAR PRODUCTE DEL CARRETÓ
@bp.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_key = str(product_id)
    if product_key in cart:
        del cart[product_key]
    session['cart'] = cart
    session.modified = True
    flash("Producte eliminat del carretó 🗑️", 'success')
    return redirect(url_for('routes.show_cart'))

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from models import db, Product, User
from werkzeug.security import generate_password_hash

# Crear carpeta instance si no existeix
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'instance'), exist_ok=True)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/techshop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    products = [
        Product(name="Auriculars Bluetooth", price=29.99, stock=20),
        Product(name="Teclat mecànic RGB", price=79.99, stock=15),
        Product(name="Ratolí ergonòmic", price=39.50, stock=10),
        Product(name="Monitor FullHD", price=199.99, stock=8),
        Product(name="Portàtil Lenovo", price=999.00, stock=5)
    ]

    user = User(
        username="ariadna",
        password_hash=generate_password_hash("password123"),
        email="ariadna@example.com"
    )

    db.session.add_all(products)
    db.session.add(user)
    db.session.commit()

    print("✅ Base de dades creada i dades de prova afegides correctament!")

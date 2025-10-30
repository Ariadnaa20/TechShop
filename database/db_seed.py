import os
import sys
from flask import Flask
from werkzeug.security import generate_password_hash

# Afegim el directori pare per poder importar models correctament
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db, Product, User

# Ruta absoluta a la base de dades (mateixa que app.py)
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'techshop.db'))

# Crear carpeta instance si no existeix
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Crear aplicació temporal
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    print("🔄 Reiniciant base de dades...")
    db.drop_all()
    db.create_all()

    # Productes de mostra
    products = [
        Product(name="Auriculars Bluetooth", price=29.99, stock=20),
        Product(name="Teclat mecànic RGB", price=79.99, stock=15),
        Product(name="Ratolí ergonòmic", price=39.50, stock=10),
        Product(name="Monitor FullHD", price=199.99, stock=8),
        Product(name="Portàtil Lenovo", price=999.00, stock=5),
    ]

    # Usuari de prova
    user = User(
        username="ariadna",
        password_hash=generate_password_hash("password123"),
        email="ariadna@example.com"
    )

    # Afegir dades i guardar
    db.session.add_all(products)
    db.session.add(user)
    db.session.commit()

    print("✅ Base de dades creada i dades de prova afegides correctament!")
    print(f"📁 Fitxer de base de dades: {db_path}")

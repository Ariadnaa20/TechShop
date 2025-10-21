# seed.py
from models.models import db, Product
from app import create_app

app = create_app()

# Entrar al context de l'aplicació Flask
with app.app_context():
    # Crear totes les taules (si encara no existeixen)
    db.create_all()

    # Llista de productes inicials amb stock
    products = [
        Product(name="Portàtil", price=1200.0, stock=10),
        Product(name="Ratolí", price=25.0, stock=50),
        Product(name="Teclat", price=50.0, stock=30),
        Product(name="Auriculars", price=75.0, stock=20),
        Product(name="Monitor", price=300.0, stock=15)
    ]

    # Afegir els productes a la sessió
    db.session.add_all(products)

    # Confirmar els canvis a la base de dades
    db.session.commit()

    print("Seed completat! S'han afegit els productes a la base de dades.")

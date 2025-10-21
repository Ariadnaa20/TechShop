from app import create_app
from models.models import db, Product, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Dades de mostra
    products = [
        Product(name="Auriculars Bluetooth", price=29.99, stock=20),
        Product(name="Teclat mecànic RGB", price=79.99, stock=15),
        Product(name="Ratolí ergonòmic", price=39.50, stock=10),
    ]

    user = User(
        username="ariadna",
        password_hash=generate_password_hash("password123"),
        email="ariadna@example.com"
    )

    db.session.add_all(products)
    db.session.add(user)
    db.session.commit()

    print("✅ Base de dades creada i dades de prova afegides!")

import os
from flask import Flask
from models import db
from routes.routes import bp


def create_app():
    app = Flask(__name__)

    # Ruta absoluta a la base de dades
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'techshop.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'unsecretkey'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

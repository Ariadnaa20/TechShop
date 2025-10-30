"""
Lògica de negoci relacionada amb els usuaris.
"""
from models import db
from models import User, db

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class UserService:
    @staticmethod
    def create_user(username: str, password: str, email: str):
        """
        Registra un nou usuari.
        Args:
            username (str)
            password (str)
            email (str)
        Raises:
            ValueError: si ja existeix username o email
        """
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            raise ValueError("L'usuari o correu ja existeix.")

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_pw, email=email, created_at=datetime.utcnow())
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def validate_user(username: str, password: str):
        """
        Valida les credencials d'un usuari.
        Returns:
            User si és correcte, sinó None.
        """
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

from db import db
from enum import Enum
from sqlalchemy import Enum as EnumType
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class UserRole(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'

class User(db.Model):  # Use Base directly
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Use PasswordType for bcrypt
    role = db.Column(EnumType(UserRole), default=UserRole.USER, nullable=False)  # Specify the length

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

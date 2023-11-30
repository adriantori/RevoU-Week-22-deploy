from enum import Enum
from sqlalchemy import Enum as EnumType
from datetime import datetime

from db import db

class TodoPriority(Enum):
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'

class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable=False)
    priority = db.Column(EnumType(TodoPriority), default=TodoPriority.LOW, nullable=False)
    due = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

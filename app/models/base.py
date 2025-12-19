"""
Базовая модель для всех моделей приложения.
Содержит общие поля: uuid, created_at, updated_at.
"""
from datetime import datetime
from uuid import uuid4
from app import db


class BaseModel(db.Model):
    """
    Абстрактная базовая модель для наследования.
    Содержит общие поля для всех моделей.
    """
    
    __abstract__ = True
    
    uuid = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
        comment="Уникальный идентификатор записи"
    )
    
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Дата и время создания записи"
    )
    
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Дата и время последнего обновления"
    )
    
    def __repr__(self) -> str:
        """Строковое представление модели."""
        return f"<{self.__class__.__name__} {self.uuid}>"


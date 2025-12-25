"""
Модель отзыва клиента.
Хранит отзывы клиентов о работе клиники.
"""
from app.models.base import BaseModel
from app import db


class Review(BaseModel):
    """
    Модель отзыва клиента о клинике.
    
    Attributes:
        name: Имя клиента
        rating: Оценка от 1 до 5
        text: Текст отзыва
        is_published: Опубликован ли отзыв
        photo_url: URL фото клиента (опционально)
    """
    
    __tablename__ = "reviews"
    
    name = db.Column(
        db.String(100),
        nullable=False,
        comment="Имя клиента"
    )
    
    rating = db.Column(
        db.Integer,
        nullable=False,
        comment="Оценка от 1 до 5"
    )
    
    text = db.Column(
        db.Text,
        nullable=False,
        comment="Текст отзыва"
    )
    
    is_published = db.Column(
        db.Boolean,
        default=True,  # Автоматическая публикация
        nullable=False,
        comment="Опубликован ли отзыв"
    )
    
    photo_url = db.Column(
        db.String(500),
        nullable=True,
        comment="URL фото клиента"
    )
    
    def __repr__(self) -> str:
        """Строковое представление отзыва."""
        return f"<Review {self.name} - {self.rating}★>"


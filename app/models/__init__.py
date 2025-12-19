"""Модуль моделей базы данных."""
from app.models.base import BaseModel
from app.models.appointment import Appointment
from app.models.review import Review

__all__ = [
    'BaseModel',
    'Appointment',
    'Review',
]


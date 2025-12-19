"""Модуль схем валидации Pydantic."""
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.schemas.review import ReviewCreate, ReviewResponse

__all__ = [
    'AppointmentCreate',
    'AppointmentResponse',
    'ReviewCreate',
    'ReviewResponse',
]


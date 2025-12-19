"""
Модель записи на консультацию.
Хранит информацию о заявках клиентов на услуги клиники.
"""
from sqlalchemy import Enum as SQLEnum
from app.models.base import BaseModel
from app import db
import enum


class AppointmentStatus(enum.Enum):
    """Статусы заявки на запись."""
    NEW = "new"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Appointment(BaseModel):
    """
    Модель заявки на запись к специалисту.
    
    Attributes:
        name: Имя клиента
        phone: Телефон клиента
        service: Выбранная услуга (опционально)
        status: Статус заявки
        agreed_to_processing: Согласие на обработку персональных данных
        agreed_to_newsletter: Согласие на получение рассылки
        comment: Дополнительный комментарий от клиента
    """
    
    __tablename__ = "appointments"
    
    name = db.Column(
        db.String(100),
        nullable=False,
        comment="Имя клиента"
    )
    
    phone = db.Column(
        db.String(20),
        nullable=False,
        comment="Телефон клиента"
    )
    
    service = db.Column(
        db.String(200),
        nullable=True,
        comment="Выбранная услуга"
    )
    
    status = db.Column(
        SQLEnum(AppointmentStatus),
        default=AppointmentStatus.NEW,
        nullable=False,
        comment="Статус заявки"
    )
    
    agreed_to_processing = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        comment="Согласие на обработку ПДн"
    )
    
    agreed_to_newsletter = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        comment="Согласие на рассылку"
    )
    
    comment = db.Column(
        db.Text,
        nullable=True,
        comment="Комментарий клиента"
    )
    
    def __repr__(self) -> str:
        """Строковое представление заявки."""
        return f"<Appointment {self.name} - {self.phone} - {self.status.value}>"


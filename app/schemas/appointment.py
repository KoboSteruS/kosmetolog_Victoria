"""
Схемы Pydantic для валидации данных записи на консультацию.
Используются для валидации входящих данных из форм.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class AppointmentCreate(BaseModel):
    """
    Схема создания заявки на запись.
    
    Attributes:
        name: Имя клиента (2-100 символов)
        phone: Телефон в формате +7XXXXXXXXXX или 8XXXXXXXXXX
        service: Выбранная услуга (опционально)
        agreed_to_processing: Обязательное согласие на обработку ПДн
        agreed_to_newsletter: Согласие на рассылку (опционально)
        comment: Комментарий клиента (опционально, до 500 символов)
    """
    
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Имя клиента",
        examples=["Анна Иванова"]
    )
    
    phone: str = Field(
        ...,
        min_length=10,
        max_length=20,
        description="Телефон клиента",
        examples=["+79991234567", "89991234567"]
    )
    
    service: Optional[str] = Field(
        None,
        max_length=200,
        description="Выбранная услуга",
        examples=["Биоревитализация лица"]
    )
    
    agreed_to_processing: bool = Field(
        ...,
        description="Согласие на обработку персональных данных (обязательно)"
    )
    
    agreed_to_newsletter: bool = Field(
        default=False,
        description="Согласие на получение рассылки"
    )
    
    comment: Optional[str] = Field(
        None,
        max_length=500,
        description="Дополнительный комментарий",
        examples=["Хочу записаться на 15:00"]
    )
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value: str) -> str:
        """
        Валидация номера телефона.
        Принимает форматы: +7XXXXXXXXXX, 8XXXXXXXXXX, 7XXXXXXXXXX
        """
        # Убираем все символы кроме цифр и +
        cleaned = re.sub(r'[^\d+]', '', value)
        
        # Проверяем формат
        if not re.match(r'^(\+7|8|7)\d{10}$', cleaned):
            raise ValueError('Некорректный формат телефона. Используйте: +79991234567 или 89991234567')
        
        # Нормализуем к формату +7XXXXXXXXXX
        if cleaned.startswith('8'):
            cleaned = '+7' + cleaned[1:]
        elif cleaned.startswith('7'):
            cleaned = '+' + cleaned
            
        return cleaned
    
    @field_validator('agreed_to_processing')
    @classmethod
    def validate_processing_agreement(cls, value: bool) -> bool:
        """Проверка обязательного согласия на обработку ПДн."""
        if not value:
            raise ValueError('Необходимо согласие на обработку персональных данных')
        return value
    
    model_config = {
        "str_strip_whitespace": True,
        "json_schema_extra": {
            "example": {
                "name": "Анна Иванова",
                "phone": "+79991234567",
                "service": "Биоревитализация лица",
                "agreed_to_processing": True,
                "agreed_to_newsletter": False,
                "comment": "Хочу записаться на 15:00"
            }
        }
    }


class AppointmentResponse(BaseModel):
    """
    Схема ответа после создания заявки.
    
    Attributes:
        uuid: Идентификатор заявки
        name: Имя клиента
        phone: Телефон клиента
        service: Выбранная услуга
        status: Статус заявки
    """
    
    uuid: str = Field(..., description="Уникальный идентификатор заявки")
    name: str = Field(..., description="Имя клиента")
    phone: str = Field(..., description="Телефон клиента")
    service: Optional[str] = Field(None, description="Выбранная услуга")
    status: str = Field(..., description="Статус заявки")
    
    model_config = {
        "from_attributes": True
    }


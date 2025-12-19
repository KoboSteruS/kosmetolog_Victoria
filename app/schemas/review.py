"""
Схемы Pydantic для валидации отзывов клиентов.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ReviewCreate(BaseModel):
    """
    Схема создания отзыва.
    
    Attributes:
        name: Имя клиента (2-100 символов)
        rating: Оценка от 1 до 5 звезд
        text: Текст отзыва (10-1000 символов)
    """
    
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Имя клиента",
        examples=["Мария Петрова"]
    )
    
    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Оценка от 1 до 5 звезд",
        examples=[5]
    )
    
    text: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Текст отзыва",
        examples=["Отличная клиника! Очень довольна результатом процедуры биоревитализации."]
    )
    
    @field_validator('rating')
    @classmethod
    def validate_rating(cls, value: int) -> int:
        """Валидация оценки."""
        if value < 1 or value > 5:
            raise ValueError('Оценка должна быть от 1 до 5')
        return value
    
    model_config = {
        "str_strip_whitespace": True,
        "json_schema_extra": {
            "example": {
                "name": "Мария Петрова",
                "rating": 5,
                "text": "Отличная клиника! Очень довольна результатом."
            }
        }
    }


class ReviewResponse(BaseModel):
    """
    Схема ответа с данными отзыва.
    
    Attributes:
        uuid: Идентификатор отзыва
        name: Имя клиента
        rating: Оценка
        text: Текст отзыва
        is_published: Опубликован ли отзыв
    """
    
    uuid: str = Field(..., description="Уникальный идентификатор отзыва")
    name: str = Field(..., description="Имя клиента")
    rating: int = Field(..., description="Оценка от 1 до 5")
    text: str = Field(..., description="Текст отзыва")
    is_published: bool = Field(..., description="Опубликован ли отзыв")
    
    model_config = {
        "from_attributes": True
    }


"""
Настройки приложения на основе Pydantic Settings.
Все настройки загружаются из переменных окружения или .env файла.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Класс настроек приложения.
    Автоматически загружает значения из переменных окружения и .env файла.
    """
    
    # Flask настройки
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    FLASK_ENV: str = "development"
    DEBUG: bool = True
    APP_NAME: str = "Victoria Clinic"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 5000
    
    # База данных
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///victoria.db"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False
    
    # Email настройки (опционально)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    ADMIN_EMAIL: Optional[str] = None
    
    # Конфигурация Pydantic
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def DATABASE_URL(self) -> str:
        """Alias для SQLALCHEMY_DATABASE_URI."""
        return self.SQLALCHEMY_DATABASE_URI


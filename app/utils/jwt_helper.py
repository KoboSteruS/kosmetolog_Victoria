"""
Утилиты для работы с JWT токенами.
Используется для авторизации в админке.
"""
import jwt
from datetime import datetime, timedelta
from typing import Optional
from loguru import logger

from app.config import settings


def generate_admin_token(expires_days: int = 365) -> str:
    """
    Генерирует JWT токен для доступа в админку.
    
    Args:
        expires_days: Срок действия токена в днях (по умолчанию 1 год)
        
    Returns:
        JWT токен в виде строки
    """
    payload = {
        'role': 'admin',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=expires_days)
    }
    
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    logger.info(f"🔑 Сгенерирован JWT токен с истечением через {expires_days} дней")
    
    return token


def verify_admin_token(token: str) -> bool:
    """
    Проверяет валидность JWT токена.
    
    Args:
        token: JWT токен для проверки
        
    Returns:
        True если токен валидный, False если нет
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        
        # Проверяем роль
        if payload.get('role') != 'admin':
            logger.warning(f"❌ Неверная роль в токене: {payload.get('role')}")
            return False
        
        logger.info(f"✅ Токен валидный, роль: {payload.get('role')}")
        return True
        
    except jwt.ExpiredSignatureError:
        logger.warning("❌ Токен истек")
        return False
    except jwt.InvalidTokenError as e:
        logger.warning(f"❌ Невалидный токен: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка при проверке токена: {e}")
        return False


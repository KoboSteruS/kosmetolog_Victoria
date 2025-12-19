"""
Точка входа для запуска Flask приложения.
Запускает сервер разработки.
"""
from app import create_app
from app.config import settings
from loguru import logger

# Создаем приложение через фабрику
app = create_app()


if __name__ == '__main__':
    logger.info(f"Запуск приложения {settings.APP_NAME}")
    logger.info(f"Режим: {'Разработка' if settings.DEBUG else 'Продакшн'}")
    logger.info(f"URL: http://{settings.APP_HOST}:{settings.APP_PORT}")
    
    app.run(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        debug=settings.DEBUG
    )


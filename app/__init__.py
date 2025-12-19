"""
Основной модуль инициализации Flask приложения.
Создает и настраивает экземпляр приложения с необходимыми расширениями.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from loguru import logger
import sys
from pathlib import Path

from app.config import settings

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()


def configure_logging() -> None:
    """
    Настройка логирования через loguru.
    Логи пишутся в файл и в консоль с разными уровнями детализации.
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Удаляем стандартный обработчик
    logger.remove()
    
    # Добавляем кастомные обработчики
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    logger.add(
        "logs/victoria_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG"
    )
    
    logger.info("Логирование успешно настроено")


def create_app() -> Flask:
    """
    Фабрика приложения Flask.
    
    Returns:
        Flask: Настроенный экземпляр приложения
    """
    app = Flask(__name__)
    
    # Загрузка конфигурации
    app.config.from_object(settings)
    
    # Настройка логирования
    configure_logging()
    logger.info("Инициализация приложения Victoria Clinic")
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Регистрация blueprints
    from app.views import main_bp
    app.register_blueprint(main_bp)
    
    logger.info("Все blueprints зарегистрированы")
    
    # Создание таблиц БД
    with app.app_context():
        db.create_all()
        logger.info("База данных инициализирована")
    
    return app


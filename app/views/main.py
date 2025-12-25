"""
Основные views приложения.
Обработка главной страницы и форм записи/отзывов.
"""
from flask import Blueprint, render_template, request, jsonify
from loguru import logger
from pydantic import ValidationError

from app import db
from app.models import Appointment, Review
from app.schemas import AppointmentCreate, ReviewCreate, AppointmentResponse, ReviewResponse
from app.services import telegram_service

main_bp = Blueprint('main', __name__)


# Данные услуг клиники с иконками
SERVICES = [
    {"name": "Прессотерапия", "price": "от 1 500 ₽", "category": "Аппаратная косметология", "icon": "fa-compress", "badge": ""},
    {"name": "Пилинг срединный", "price": "от 4 700 ₽", "category": "Пилинги", "icon": "fa-layer-group", "badge": ""},
    {"name": "Биоревитализация лица", "price": "от 7 000 ₽", "category": "Инъекционные процедуры", "icon": "fa-syringe", "badge": "Популярно"},
    {"name": "Мезотерапия лица", "price": "от 5 000 ₽", "category": "Инъекционные процедуры", "icon": "fa-syringe", "badge": ""},
    {"name": "Мезотерапия головы", "price": "от 4 800 ₽", "category": "Инъекционные процедуры", "icon": "fa-head-side-virus", "badge": ""},
    {"name": "Фотолечение / фототерапия", "price": "от 3 200 ₽", "category": "Аппаратная косметология", "icon": "fa-lightbulb", "badge": ""},
    {"name": "Уходовая линия Line Repair (CHRISTINA)", "price": "от 4 900 ₽", "category": "Косметология", "icon": "fa-spa", "badge": ""},
    {"name": "Чистка лица атравматическая", "price": "от 5 700 ₽", "category": "Косметология", "icon": "fa-hands-wash", "badge": ""},
    {"name": "Чистка лица комбинированная", "price": "от 3 800 ₽", "category": "Косметология", "icon": "fa-hands-wash", "badge": "Популярно"},
    {"name": "Чистка лица ультразвуковая", "price": "от 2 000 ₽", "category": "Косметология", "icon": "fa-hand-sparkles", "badge": ""},
    {"name": "Пилинг поверхностный", "price": "от 2 500 ₽", "category": "Пилинги", "icon": "fa-layer-group", "badge": ""},
    {"name": "LPG-массаж", "price": "от 700 ₽", "category": "Массажи лица", "icon": "fa-hands", "badge": ""},
    {"name": "Пилинг карбоновый", "price": "от 3 500 ₽", "category": "Пилинги", "icon": "fa-atom", "badge": ""},
    {"name": "Ручной массаж лица", "price": "от 1 800 ₽", "category": "Массажи лица", "icon": "fa-hand-holding-heart", "badge": ""},
    {"name": "RF-лифтинг", "price": "от 2 300 ₽", "category": "Аппаратная косметология", "icon": "fa-bolt", "badge": "Популярно"},
    {"name": "Пилинг алмазный", "price": "от 3 000 ₽", "category": "Пилинги", "icon": "fa-gem", "badge": ""},
    {"name": "Вакуумный массаж лица", "price": "от 2 300 ₽", "category": "Массажи лица", "icon": "fa-circle-notch", "badge": ""},
    {"name": "Альгинатная маска", "price": "от 1 200 ₽", "category": "Косметология", "icon": "fa-mask", "badge": ""},
    {"name": "Регенерация кожи", "price": "от 2 800 ₽", "category": "Косметология", "icon": "fa-seedling", "badge": ""},
    {"name": "Глубокое увлажнение", "price": "от 3 700 ₽", "category": "Косметология", "icon": "fa-tint", "badge": ""},
    {"name": "Безинъекционная мезотерапия", "price": "от 2 200 ₽", "category": "Косметология", "icon": "fa-magic", "badge": ""},
    {"name": "Лазерная эпиляция", "price": "от 600 ₽", "category": "Аппаратная косметология", "icon": "fa-fire", "badge": ""},
    {"name": "Карбокситерапия", "price": "от 2 500 ₽", "category": "Инъекционные процедуры", "icon": "fa-wind", "badge": ""},
    {"name": "Микротоковая терапия", "price": "от 2 200 ₽", "category": "Аппаратная косметология", "icon": "fa-broadcast-tower", "badge": ""},
]

# Данные специалистов
SPECIALISTS = [
    {
        "name": "Ведущий косметолог",
        "position": "Главный врач-косметолог",
        "specialization": "Клиника косметологии и коррекции фигуры",
        "image": "doctor1.png",
        "experience": "Более 15 лет опыта"
    },
    {
        "name": "Косметолог клиники",
        "position": "Врач-косметолог",
        "specialization": "Специалист по инъекционным методикам и уходам",
        "image": "doctor2.png",
        "experience": "Медицинское образование"
    },
    {
        "name": "Специалист по LPG",
        "position": "Врач-косметолог",
        "specialization": "Аппаратная косметология и коррекция фигуры",
        "image": "doctor3.png",
        "experience": "Медицинское образование"
    },
    {
        "name": "Косметолог",
        "position": "Врач-косметолог",
        "specialization": "Пилинги, чистки и лазерная эпиляция",
        "image": "doctor4.png",
        "experience": "Медицинское образование"
    },
]


@main_bp.route('/')
def index():
    """
    Главная страница лендинга.
    
    Returns:
        HTML страница с данными услуг, специалистов и опубликованных отзывов
    """
    logger.info("Загрузка главной страницы")
    
    # Получаем опубликованные отзывы
    reviews = Review.query.filter_by(is_published=True).order_by(Review.created_at.desc()).limit(10).all()
    
    return render_template(
        'index.html',
        services=SERVICES,
        specialists=SPECIALISTS,
        reviews=reviews
    )


@main_bp.route('/api/appointments', methods=['POST'])
def create_appointment():
    """
    API endpoint для создания заявки на запись.
    
    Returns:
        JSON с данными созданной заявки или ошибками валидации
    """
    try:
        # Получаем данные из формы
        data = request.get_json()
        logger.info(f"Получена заявка на запись: {data.get('name', 'unknown')}")
        
        # Валидируем данные через Pydantic
        appointment_data = AppointmentCreate(**data)
        
        # Создаем запись в БД
        appointment = Appointment(
            name=appointment_data.name,
            phone=appointment_data.phone,
            service=appointment_data.service,
            agreed_to_processing=appointment_data.agreed_to_processing,
            agreed_to_newsletter=appointment_data.agreed_to_newsletter,
            comment=appointment_data.comment
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        logger.success(f"Заявка успешно создана: {appointment.uuid}")
        
        # Отправляем уведомление в Telegram
        try:
            message = telegram_service.format_appointment_message(
                name=appointment_data.name,
                phone=appointment_data.phone,
                service=appointment_data.service,
                comment=appointment_data.comment
            )
            result = telegram_service.send_to_all(message)
            logger.info(
                f"Уведомление отправлено в Telegram: "
                f"{result['success']} успешно, {result['failed']} ошибок"
            )
        except Exception as e:
            # Не прерываем процесс если отправка в Telegram не удалась
            logger.error(f"Ошибка отправки в Telegram: {e}")
        
        # Формируем ответ
        response_data = AppointmentResponse.model_validate(appointment)
        
        return jsonify({
            "success": True,
            "message": "Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.",
            "data": response_data.model_dump()
        }), 201
        
    except ValidationError as e:
        logger.warning(f"Ошибка валидации заявки: {e}")
        return jsonify({
            "success": False,
            "message": "Ошибка валидации данных",
            "errors": e.errors()
        }), 400
        
    except Exception as e:
        logger.error(f"Ошибка при создании заявки: {e}")
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Произошла ошибка при обработке заявки. Попробуйте позже."
        }), 500


@main_bp.route('/api/reviews', methods=['POST'])
def create_review():
    """
    API endpoint для создания отзыва.
    
    Returns:
        JSON с данными созданного отзыва или ошибками валидации
    """
    try:
        # Получаем данные из формы
        data = request.get_json()
        logger.info(f"Получен отзыв от: {data.get('name', 'unknown')}")
        
        # Валидируем данные через Pydantic
        review_data = ReviewCreate(**data)
        
        # Создаем отзыв в БД (по умолчанию не опубликован)
        review = Review(
            name=review_data.name,
            rating=review_data.rating,
            text=review_data.text,
            is_published=False  # Требует модерации
        )
        
        db.session.add(review)
        db.session.commit()
        
        logger.success(f"Отзыв успешно создан: {review.uuid}")
        
        # Формируем ответ
        response_data = ReviewResponse.model_validate(review)
        
        return jsonify({
            "success": True,
            "message": "Спасибо за ваш отзыв! Он появится на сайте после модерации.",
            "data": response_data.model_dump()
        }), 201
        
    except ValidationError as e:
        logger.warning(f"Ошибка валидации отзыва: {e}")
        return jsonify({
            "success": False,
            "message": "Ошибка валидации данных",
            "errors": e.errors()
        }), 400
        
    except Exception as e:
        logger.error(f"Ошибка при создании отзыва: {e}")
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Произошла ошибка при отправке отзыва. Попробуйте позже."
        }), 500


@main_bp.route('/api/reviews', methods=['GET'])
def get_reviews():
    """
    API endpoint для получения списка опубликованных отзывов.
    
    Returns:
        JSON со списком отзывов
    """
    try:
        reviews = Review.query.filter_by(is_published=True).order_by(Review.created_at.desc()).all()
        
        reviews_data = [ReviewResponse.model_validate(review).model_dump() for review in reviews]
        
        return jsonify({
            "success": True,
            "data": reviews_data
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка при получении отзывов: {e}")
        return jsonify({
            "success": False,
            "message": "Ошибка при загрузке отзывов"
        }), 500


"""
Основные views приложения.
Обработка главной страницы и форм записи/отзывов.
"""
from flask import Blueprint, render_template, request, jsonify, abort
from loguru import logger
from pydantic import ValidationError

from app import db
from app.models import Appointment, Review
from app.schemas import AppointmentCreate, ReviewCreate, AppointmentResponse, ReviewResponse
from app.services import telegram_service
from app.utils import verify_admin_token

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
        "name": "Надежда",
        "position": "Врач-косметолог",
        "specialization": "Эстетическая косметология",
        "image": "doctor1.jpg",
        "experience": "Более 15 лет опыта",
        "description": "Наш улыбчивый и заботливый косметолог!",
        "education": [
            {
                "year": "2010",
                "text": "Окончен «Петрозаводский базовый медицинский колледж» по специальности «сестринское дело»"
            },
            {
                "year": "2012",
                "text": "Выдан сертификат по специальности «медицинский массаж»"
            },
            {
                "year": "2019",
                "text": "АНО «Северо-западная косметологическая школа» - базовый курс по эстетической косметологии, присвоена квалификация косметик третьего разряда"
            },
            {
                "year": "2021",
                "text": "Курс «секреты успешного косметолога»"
            }
        ],
        "quote": None
    },
    {
        "name": "Татьяна Буданова",
        "position": "Врач-косметолог",
        "specialization": "Специалист по инъекционным методикам и уходам",
        "image": "doctor2.jpg",
        "experience": "Опытный специалист",
        "description": "Специалист своего дела с опытом работы и заботой о каждом клиенте!",
        "education": [
            {
                "year": "2008",
                "text": "Петрозаводский Базовый Медицинский Колледж - работа в Родильном доме им. Гудкина К.А."
            },
            {
                "year": "2019",
                "text": "Высшее образование - Академия государственной службы при Президенте РФ (государственное и муниципальное управление)"
            },
            {
                "year": "2020",
                "text": "Диплом «Сестринское дело в косметологии»"
            },
            {
                "year": "2022-2025",
                "text": "Работала в студии DPSP «Лицо и Тело» в качестве косметолога"
            }
        ],
        "procedures": [
            "Массажи лица, шеи, зоны декольте",
            "Пилинги",
            "Микродермабразия",
            "Чистки лица (механическая, комбинированная, УЗК)",
            "УЗК кавитация",
            "Вакуумный массаж лица и тела",
            "Радиочастотный лифтинг",
            "Микротоковая терапия",
            "Мезотерапия безынъекционная",
            "Лазерная эпиляция",
            "LPG массаж",
            "Карбоновый пилинг",
            "Карбокситерапия"
        ],
        "quote": "Записи к Татьяне открыта с 10 августа"
    },
    {
        "name": "Ирина Карелина",
        "position": "Врач-косметолог",
        "specialization": "Аппаратная косметология и коррекция фигуры",
        "image": "doctor3.jpeg",
        "experience": "Опытный специалист",
        "description": "Я учусь непрерывно и иду дальше, развиваясь в направлении медицины. Пришла в косметологию по любви.",
        "education": [
            {
                "year": "2013",
                "text": "«Петрозаводский базовый медицинский колледж» - Диплом по специальности «Сестринское дело»"
            },
            {
                "year": "2014",
                "text": "«Петрозаводский базовый медицинский колледж» - «Медицинский массаж»"
            },
            {
                "year": "2024",
                "text": "Удостоверение о повышении квалификации «Сестринское дело»"
            },
            {
                "year": "2025",
                "text": "Курсы «косметолог-эстетист» в Международном университете профессиональной подготовки"
            }
        ],
        "quote": "Все больше и больше девушек выбирают именно Ирину!"
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


@main_bp.route('/api/telegram/test', methods=['GET'])
def test_telegram():
    """
    API endpoint для тестирования Telegram интеграции.
    Показывает активные chat_id и последние обновления.
    
    Returns:
        JSON с информацией о Telegram чатах
    """
    try:
        # Получаем обновления
        updates = telegram_service.get_updates()
        
        # Получаем активные chat_id
        active_chats = telegram_service.get_active_chat_ids()
        
        # Форматируем информацию об обновлениях
        updates_info = []
        for update in updates[-10:]:  # Последние 10
            if 'message' in update:
                msg = update['message']
                updates_info.append({
                    'chat_id': msg['chat']['id'],
                    'username': msg['chat'].get('username', 'N/A'),
                    'first_name': msg['chat'].get('first_name', 'N/A'),
                    'text': msg.get('text', 'N/A'),
                    'date': msg.get('date', 'N/A')
                })
        
        return jsonify({
            'success': True,
            'active_chats': active_chats,
            'active_chats_count': len(active_chats),
            'recent_updates': updates_info,
            'total_updates': len(updates),
            'message': f'Найдено {len(active_chats)} активных чатов'
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка при тестировании Telegram: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
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


@main_bp.route('/api/reviews/all', methods=['GET'])
def get_all_reviews():
    """
    API endpoint для получения ВСЕХ отзывов (включая неопубликованные).
    Для модерации.
    
    Returns:
        JSON со списком всех отзывов
    """
    try:
        reviews = Review.query.order_by(Review.created_at.desc()).all()
        
        reviews_data = []
        for review in reviews:
            review_dict = ReviewResponse.model_validate(review).model_dump()
            review_dict['is_published'] = review.is_published
            review_dict['uuid'] = str(review.uuid)
            reviews_data.append(review_dict)
        
        return jsonify({
            "success": True,
            "total": len(reviews_data),
            "published": len([r for r in reviews_data if r['is_published']]),
            "unpublished": len([r for r in reviews_data if not r['is_published']]),
            "data": reviews_data
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка при получении всех отзывов: {e}")
        return jsonify({
            "success": False,
            "message": "Ошибка при загрузке отзывов"
        }), 500


@main_bp.route('/api/reviews/<uuid>/publish', methods=['POST'])
def publish_review(uuid):
    """
    API endpoint для публикации отзыва.
    
    Args:
        uuid: UUID отзыва
        
    Returns:
        JSON с результатом операции
    """
    try:
        review = Review.query.filter_by(uuid=uuid).first()
        
        if not review:
            return jsonify({
                "success": False,
                "message": "Отзыв не найден"
            }), 404
        
        review.is_published = True
        db.session.commit()
        
        logger.success(f"Отзыв {uuid} опубликован")
        
        return jsonify({
            "success": True,
            "message": "Отзыв успешно опубликован"
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка при публикации отзыва: {e}")
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Ошибка при публикации отзыва"
        }), 500


@main_bp.route('/api/reviews/<uuid>/unpublish', methods=['POST'])
def unpublish_review(uuid):
    """
    API endpoint для скрытия отзыва.
    
    Args:
        uuid: UUID отзыва
        
    Returns:
        JSON с результатом операции
    """
    try:
        review = Review.query.filter_by(uuid=uuid).first()
        
        if not review:
            return jsonify({
                "success": False,
                "message": "Отзыв не найден"
            }), 404
        
        review.is_published = False
        db.session.commit()
        
        logger.success(f"Отзыв {uuid} скрыт")
        
        return jsonify({
            "success": True,
            "message": "Отзыв успешно скрыт"
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка при скрытии отзыва: {e}")
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Ошибка при скрытии отзыва"
        }), 500


@main_bp.route('/api/reviews/<uuid>', methods=['DELETE'])
def delete_review(uuid):
    """
    API endpoint для удаления отзыва.
    
    Args:
        uuid: UUID отзыва
        
    Returns:
        JSON с результатом операции
    """
    try:
        review = Review.query.filter_by(uuid=uuid).first()
        
        if not review:
            return jsonify({
                "success": False,
                "message": "Отзыв не найден"
            }), 404
        
        review_name = review.name
        db.session.delete(review)
        db.session.commit()
        
        logger.success(f"Отзыв {uuid} от {review_name} удален")
        
        return jsonify({
            "success": True,
            "message": f"Отзыв от {review_name} успешно удален"
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка при удалении отзыва: {e}")
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Ошибка при удалении отзыва"
        }), 500


@main_bp.route('/<token>/admin')
def admin_panel(token):
    """
    Админ-панель для управления отзывами.
    Доступ по JWT токену в URL.
    
    Args:
        token: JWT токен для авторизации
        
    Returns:
        HTML страница админки или 403
    """
    logger.info(f"🔐 Попытка доступа в админку с токеном: {token[:20]}...")
    
    # Проверяем токен
    if not verify_admin_token(token):
        logger.warning(f"❌ Доступ в админку запрещен: невалидный токен")
        abort(403, description="Доступ запрещен. Неверный токен.")
    
    logger.success(f"✅ Доступ в админку разрешен")
    return render_template('admin.html', token=token)


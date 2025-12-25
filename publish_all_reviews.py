"""
Скрипт для публикации всех неопубликованных отзывов.
Полезно для разового запуска после изменения логики.
"""
from app import create_app, db
from app.models import Review
from loguru import logger

def publish_all_reviews():
    """Публикует все неопубликованные отзывы."""
    app = create_app()
    
    with app.app_context():
        # Находим все неопубликованные отзывы
        unpublished = Review.query.filter_by(is_published=False).all()
        
        if not unpublished:
            logger.info("✅ Нет неопубликованных отзывов")
            return
        
        logger.info(f"📋 Найдено {len(unpublished)} неопубликованных отзывов")
        
        # Публикуем все
        for review in unpublished:
            review.is_published = True
            logger.info(f"  ✅ Опубликован отзыв от {review.name} ({review.rating}★)")
        
        db.session.commit()
        logger.success(f"🎉 Успешно опубликовано {len(unpublished)} отзывов!")
        
        # Показываем статистику
        total = Review.query.count()
        published = Review.query.filter_by(is_published=True).count()
        
        logger.info(f"\n📊 Статистика:")
        logger.info(f"   Всего отзывов: {total}")
        logger.info(f"   Опубликовано: {published}")
        logger.info(f"   Скрыто: {total - published}")


if __name__ == "__main__":
    publish_all_reviews()


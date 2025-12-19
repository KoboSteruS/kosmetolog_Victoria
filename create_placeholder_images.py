"""
Скрипт для создания placeholder изображений.
Создает заглушки для фото клиники и специалистов с красивым дизайном.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Цвета в соответствии с палитрой
PRIMARY_COLOR = (200, 123, 133)  # #C87B85
SECONDARY_COLOR = (245, 233, 233)  # #F5E9E9
DARK_COLOR = (44, 27, 27)  # #2C1B1B

def create_placeholder(width: int, height: int, text: str, filename: str):
    """
    Создает красивое placeholder изображение.
    
    Args:
        width: Ширина изображения
        height: Высота изображения
        text: Текст на изображении
        filename: Имя файла для сохранения
    """
    # Создаем изображение с градиентом
    img = Image.new('RGB', (width, height), SECONDARY_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Рисуем градиент
    for i in range(height):
        ratio = i / height
        r = int(SECONDARY_COLOR[0] + (PRIMARY_COLOR[0] - SECONDARY_COLOR[0]) * ratio)
        g = int(SECONDARY_COLOR[1] + (PRIMARY_COLOR[1] - SECONDARY_COLOR[1]) * ratio)
        b = int(SECONDARY_COLOR[2] + (PRIMARY_COLOR[2] - SECONDARY_COLOR[2]) * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Добавляем текст
    try:
        # Пытаемся использовать красивый шрифт
        font_size = 40 if width > 500 else 30
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Если не получилось, используем стандартный
        font = ImageFont.load_default()
    
    # Рисуем полупрозрачный прямоугольник под текстом
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    padding = 20
    rect_x1 = (width - text_width) // 2 - padding
    rect_y1 = (height - text_height) // 2 - padding
    rect_x2 = (width + text_width) // 2 + padding
    rect_y2 = (height + text_height) // 2 + padding
    
    # Рисуем прямоугольник
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(
        [rect_x1, rect_y1, rect_x2, rect_y2],
        fill=(*DARK_COLOR, 180)
    )
    
    # Накладываем overlay
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, overlay)
    img = img.convert('RGB')
    
    # Рисуем текст
    draw = ImageDraw.Draw(img)
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    
    # Сохраняем
    output_path = Path('app/static/images') / filename
    img.save(output_path, quality=85, optimize=True)
    print(f"✅ Создан: {filename}")


def main():
    """Создает все необходимые placeholder изображения."""
    
    print("🎨 Создание placeholder изображений...\n")
    
    # Создаем папку если её нет
    images_dir = Path('app/static/images')
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Фотографии клиники (горизонтальные)
    print("📸 Создание фото клиники...")
    create_placeholder(800, 600, "Интерьер клиники", "clinic1.jpg")
    create_placeholder(800, 600, "Кабинет косметолога", "clinic2.jpg")
    create_placeholder(800, 600, "Процедурный кабинет", "clinic3.jpg")
    
    print("\n👨‍⚕️ Создание фото специалистов...")
    # Фотографии специалистов (вертикальные)
    create_placeholder(400, 500, "Елена Васильева", "doctor1.jpg")
    create_placeholder(400, 500, "Виктория Коваленко", "doctor2.jpg")
    create_placeholder(400, 500, "Ксения Михайлова", "doctor3.jpg")
    create_placeholder(400, 500, "Ольга Андреева", "doctor4.jpg")
    
    print("\n🎉 Готово! Все изображения созданы.")
    print("Теперь можно запускать приложение: python run.py")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("❌ Ошибка: не установлена библиотека Pillow")
        print("Установите её командой: pip install Pillow")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


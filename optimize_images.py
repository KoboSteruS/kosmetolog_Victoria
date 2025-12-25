"""
Скрипт для оптимизации изображений сайта.
Конвертирует PNG в WebP с fallback для старых браузеров.

Использование:
    pip install Pillow
    python optimize_images.py
"""
from pathlib import Path
from PIL import Image
import os

def optimize_image(image_path: Path, quality: int = 85) -> None:
    """
    Оптимизирует изображение: создает WebP версию.
    
    Args:
        image_path: Путь к изображению
        quality: Качество сжатия (0-100)
    """
    try:
        # Открываем изображение
        img = Image.open(image_path)
        
        # Конвертируем в RGB если нужно
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Создаем WebP версию
        webp_path = image_path.with_suffix('.webp')
        img.save(webp_path, 'WebP', quality=quality, method=6)
        
        original_size = image_path.stat().st_size
        webp_size = webp_path.stat().st_size
        saved = ((original_size - webp_size) / original_size) * 100
        
        print(f"✓ {image_path.name} → {webp_path.name} (сохранено {saved:.1f}%)")
        
    except Exception as e:
        print(f"✗ Ошибка при обработке {image_path}: {e}")


def optimize_all_images(images_dir: str = "app/static/images") -> None:
    """
    Оптимизирует все PNG изображения в директории.
    
    Args:
        images_dir: Путь к директории с изображениями
    """
    images_path = Path(images_dir)
    
    if not images_path.exists():
        print(f"Директория {images_dir} не найдена!")
        return
    
    png_files = list(images_path.glob("*.png"))
    
    if not png_files:
        print("PNG файлы не найдены!")
        return
    
    print(f"Найдено {len(png_files)} PNG файлов. Начинаем оптимизацию...\n")
    
    for png_file in png_files:
        optimize_image(png_file)
    
    print(f"\n✅ Оптимизация завершена! Обработано {len(png_files)} файлов.")
    print("\nТеперь обновите HTML шаблоны для использования WebP с fallback:")
    print("<picture>")
    print('  <source srcset="image.webp" type="image/webp">')
    print('  <img src="image.png" alt="...">')
    print("</picture>")


if __name__ == "__main__":
    optimize_all_images()


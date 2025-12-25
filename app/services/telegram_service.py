"""
Сервис для отправки уведомлений в Telegram.
Отправляет заявки с сайта всем пользователям, которые начали чат с ботом.
"""
import requests
from typing import List, Optional
from loguru import logger

from app.config import settings


class TelegramService:
    """Сервис для работы с Telegram Bot API."""
    
    def __init__(self):
        """Инициализация сервиса."""
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.chat_ids = self._parse_chat_ids(settings.TELEGRAM_CHAT_IDS)
    
    def _parse_chat_ids(self, chat_ids_str: str) -> List[str]:
        """
        Парсит строку с chat_id в список.
        
        Args:
            chat_ids_str: Строка с chat_id через запятую
            
        Returns:
            Список chat_id
        """
        if not chat_ids_str:
            return []
        return [cid.strip() for cid in chat_ids_str.split(',') if cid.strip()]
    
    def get_updates(self, limit: int = 100) -> List[dict]:
        """
        Получает обновления от бота (новые сообщения).
        Используется для получения chat_id пользователей.
        
        Args:
            limit: Максимальное количество обновлений для получения
            
        Returns:
            Список обновлений
        """
        logger.info(f"🤖 [TELEGRAM] Запрос getUpdates с limit={limit}")
        logger.info(f"🤖 [TELEGRAM] URL: {self.base_url}/getUpdates")
        
        try:
            params = {
                'limit': limit,
                'offset': 0
            }
            logger.info(f"🤖 [TELEGRAM] Параметры запроса: {params}")
            
            response = requests.get(
                f"{self.base_url}/getUpdates",
                params=params,
                timeout=10
            )
            
            logger.info(f"🤖 [TELEGRAM] HTTP Status: {response.status_code}")
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"🤖 [TELEGRAM] Ответ API - ok: {data.get('ok')}")
            logger.info(f"🤖 [TELEGRAM] Количество обновлений: {len(data.get('result', []))}")
            
            if data.get('ok'):
                updates = data.get('result', [])
                logger.info(f"✅ [TELEGRAM] Получено {len(updates)} обновлений")
                
                # Логируем детали каждого обновления
                for i, update in enumerate(updates):
                    if 'message' in update:
                        msg = update['message']
                        chat = msg.get('chat', {})
                        logger.info(
                            f"  📩 Обновление {i+1}: "
                            f"chat_id={chat.get('id')}, "
                            f"username=@{chat.get('username', 'N/A')}, "
                            f"text='{msg.get('text', 'N/A')[:50]}'"
                        )
                
                return updates
            else:
                error_desc = data.get('description', 'Unknown error')
                logger.error(f"❌ [TELEGRAM] Ошибка API: {error_desc}")
                logger.error(f"❌ [TELEGRAM] Полный ответ: {data}")
                return []
            
        except Exception as e:
            logger.error(f"❌ [TELEGRAM] Исключение при getUpdates: {e}")
            logger.error(f"❌ [TELEGRAM] Тип: {type(e).__name__}")
            return []
    
    def get_active_chat_ids(self) -> List[str]:
        """
        Получает список chat_id пользователей, которые писали боту.
        Комбинирует chat_id из настроек и из последних обновлений.
        
        Returns:
            Список уникальных chat_id
        """
        logger.info("🔍 [TELEGRAM] Поиск активных chat_id...")
        chat_ids = set()
        
        # Добавляем chat_id из настроек (если есть)
        logger.info(f"🔍 [TELEGRAM] Проверяем настройки TELEGRAM_CHAT_IDS...")
        if self.chat_ids:
            chat_ids.update(self.chat_ids)
            logger.info(f"✅ [TELEGRAM] Найдено в настройках: {self.chat_ids}")
        else:
            logger.info(f"ℹ️  [TELEGRAM] В настройках нет сохраненных chat_id")
        
        # Получаем chat_id из последних обновлений
        logger.info(f"🔍 [TELEGRAM] Запрашиваем обновления от бота...")
        updates = self.get_updates()
        logger.info(f"📊 [TELEGRAM] Получено обновлений для обработки: {len(updates)}")
        
        if not updates:
            logger.warning("⚠️  [TELEGRAM] Нет обновлений от бота!")
            logger.warning("⚠️  [TELEGRAM] Возможные причины:")
            logger.warning("   1. Никто не писал боту")
            logger.warning("   2. Обновления уже были обработаны")
            logger.warning("   3. Неверный токен бота")
        
        found_in_updates = 0
        for i, update in enumerate(updates, 1):
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                username = update['message']['chat'].get('username', 'N/A')
                first_name = update['message']['chat'].get('first_name', 'N/A')
                text = update['message'].get('text', 'N/A')
                
                chat_ids.add(str(chat_id))
                found_in_updates += 1
                
                logger.info(
                    f"  ✅ Обновление {i}: "
                    f"chat_id={chat_id}, "
                    f"username=@{username}, "
                    f"имя={first_name}, "
                    f"сообщение='{text[:30]}'"
                )
        
        result = list(chat_ids)
        
        logger.info("=" * 60)
        logger.info(f"📊 [TELEGRAM] ИТОГО найдено chat_id:")
        logger.info(f"   - Из настроек: {len(self.chat_ids)}")
        logger.info(f"   - Из обновлений: {found_in_updates}")
        logger.info(f"   - Всего уникальных: {len(result)}")
        logger.info(f"   - Список: {result}")
        logger.info("=" * 60)
        
        return result
    
    def send_message(
        self,
        chat_id: str,
        text: str,
        parse_mode: str = "HTML"
    ) -> bool:
        """
        Отправляет сообщение в Telegram чат.
        
        Args:
            chat_id: ID чата Telegram
            text: Текст сообщения
            parse_mode: Режим парсинга (HTML или Markdown)
            
        Returns:
            True если успешно, False если ошибка
        """
        logger.info(f"🤖 [TELEGRAM] Попытка отправить сообщение в chat_id: {chat_id}")
        logger.info(f"🤖 [TELEGRAM] URL: {self.base_url}/sendMessage")
        logger.info(f"🤖 [TELEGRAM] Текст сообщения (первые 100 символов): {text[:100]}...")
        
        try:
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode
            }
            logger.info(f"🤖 [TELEGRAM] Payload: {payload}")
            
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json=payload,
                timeout=10
            )
            
            logger.info(f"🤖 [TELEGRAM] HTTP Status Code: {response.status_code}")
            logger.info(f"🤖 [TELEGRAM] Response: {response.text}")
            
            response.raise_for_status()
            
            data = response.json()
            if data.get('ok'):
                logger.success(f"✅ [TELEGRAM] Сообщение успешно отправлено в chat {chat_id}")
                return True
            else:
                logger.error(f"❌ [TELEGRAM] Ошибка API: {data.get('description')}")
                logger.error(f"❌ [TELEGRAM] Полный ответ: {data}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ [TELEGRAM] Ошибка HTTP запроса: {e}")
            logger.error(f"❌ [TELEGRAM] Тип ошибки: {type(e).__name__}")
            return False
        except Exception as e:
            logger.error(f"❌ [TELEGRAM] Неожиданная ошибка: {e}")
            logger.error(f"❌ [TELEGRAM] Тип ошибки: {type(e).__name__}")
            return False
    
    def send_to_all(self, text: str) -> dict:
        """
        Отправляет сообщение всем пользователям, которые писали боту.
        
        Args:
            text: Текст сообщения
            
        Returns:
            Словарь с результатами отправки
        """
        logger.info("=" * 80)
        logger.info("🚀 [TELEGRAM] Начало рассылки уведомления")
        logger.info("=" * 80)
        
        # Получаем актуальный список chat_id
        logger.info("📋 [TELEGRAM] Получаем список активных чатов...")
        active_chats = self.get_active_chat_ids()
        
        logger.info(f"📊 [TELEGRAM] Найдено активных чатов: {len(active_chats)}")
        logger.info(f"📊 [TELEGRAM] Chat IDs: {active_chats}")
        
        if not active_chats:
            logger.warning("⚠️  [TELEGRAM] Нет активных чатов для отправки уведомлений!")
            logger.warning("⚠️  [TELEGRAM] Убедитесь что кто-то написал боту /start")
            return {
                'success': 0,
                'failed': 0,
                'total': 0,
                'message': 'Нет пользователей, которые начали чат с ботом'
            }
        
        logger.info(f"📤 [TELEGRAM] Начинаем рассылку в {len(active_chats)} чатов...")
        
        success_count = 0
        failed_count = 0
        
        for i, chat_id in enumerate(active_chats, 1):
            logger.info(f"\n--- Отправка {i}/{len(active_chats)} ---")
            if self.send_message(chat_id, text):
                success_count += 1
                logger.success(f"✅ [TELEGRAM] Отправлено в чат {chat_id} ({i}/{len(active_chats)})")
            else:
                failed_count += 1
                logger.error(f"❌ [TELEGRAM] Не удалось отправить в чат {chat_id} ({i}/{len(active_chats)})")
        
        logger.info("\n" + "=" * 80)
        logger.info(
            f"🏁 [TELEGRAM] Рассылка завершена: "
            f"✅ {success_count} успешно | "
            f"❌ {failed_count} ошибок | "
            f"📊 Всего: {len(active_chats)}"
        )
        logger.info("=" * 80)
        
        return {
            'success': success_count,
            'failed': failed_count,
            'total': len(active_chats)
        }
    
    def format_appointment_message(
        self,
        name: str,
        phone: str,
        service: Optional[str] = None,
        comment: Optional[str] = None
    ) -> str:
        """
        Форматирует сообщение о записи на прием.
        
        Args:
            name: Имя клиента
            phone: Телефон клиента
            service: Услуга (опционально)
            comment: Комментарий (опционально)
            
        Returns:
            Отформатированное сообщение
        """
        message = "🆕 <b>Новая заявка на запись!</b>\n\n"
        message += f"👤 <b>Имя:</b> {name}\n"
        message += f"📱 <b>Телефон:</b> {phone}\n"
        
        if service:
            message += f"💅 <b>Услуга:</b> {service}\n"
        
        if comment:
            message += f"💬 <b>Комментарий:</b> {comment}\n"
        
        message += f"\n📅 <i>Не забудьте связаться с клиентом!</i>"
        
        return message


# Создаем глобальный экземпляр сервиса
telegram_service = TelegramService()


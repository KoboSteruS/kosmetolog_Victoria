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
    
    def get_updates(self) -> List[dict]:
        """
        Получает обновления от бота (новые сообщения).
        Используется для получения chat_id пользователей.
        
        Returns:
            Список обновлений
        """
        try:
            response = requests.get(
                f"{self.base_url}/getUpdates",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('ok'):
                return data.get('result', [])
            return []
            
        except Exception as e:
            logger.error(f"Ошибка при получении обновлений Telegram: {e}")
            return []
    
    def get_active_chat_ids(self) -> List[str]:
        """
        Получает список chat_id пользователей, которые писали боту.
        
        Returns:
            Список уникальных chat_id
        """
        updates = self.get_updates()
        chat_ids = set()
        
        for update in updates:
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                chat_ids.add(str(chat_id))
        
        return list(chat_ids)
    
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
        try:
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": parse_mode
                },
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get('ok'):
                logger.info(f"Сообщение отправлено в Telegram chat {chat_id}")
                return True
            else:
                logger.error(f"Ошибка Telegram API: {data.get('description')}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при отправке в Telegram: {e}")
            return False
    
    def send_to_all(self, text: str) -> dict:
        """
        Отправляет сообщение всем пользователям, которые писали боту.
        
        Args:
            text: Текст сообщения
            
        Returns:
            Словарь с результатами отправки
        """
        # Получаем актуальный список chat_id
        active_chats = self.get_active_chat_ids()
        
        if not active_chats:
            logger.warning("Нет активных чатов для отправки уведомлений")
            return {
                'success': 0,
                'failed': 0,
                'total': 0,
                'message': 'Нет пользователей, которые начали чат с ботом'
            }
        
        success_count = 0
        failed_count = 0
        
        for chat_id in active_chats:
            if self.send_message(chat_id, text):
                success_count += 1
            else:
                failed_count += 1
        
        logger.info(
            f"Отправка завершена: {success_count} успешно, "
            f"{failed_count} ошибок из {len(active_chats)} чатов"
        )
        
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


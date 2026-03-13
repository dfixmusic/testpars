import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Config:
    """Конфигурация для Telegram парсера"""
    
    # API данные Telegram
    API_ID = int(os.getenv('API_ID', 0))
    API_HASH = os.getenv('API_HASH', '')
    PHONE = os.getenv('PHONE', '')
    
    # Каналы для парсинга
    CHANNELS = [channel.strip() for channel in os.getenv('CHANNELS', '').split(',') if channel.strip()]
    
    # Ключевые слова для поиска
    KEYWORDS = [keyword.strip().lower() for keyword in os.getenv('KEYWORDS', '').split(',') if keyword.strip()]
    
    # Файл сессии
    SESSION_FILE = 'telegram_session'
    
    @classmethod
    def validate(cls):
        """Проверяет корректность конфигурации"""
        if not cls.API_ID or not cls.API_HASH:
            raise ValueError("API_ID и API_HASH обязательны! Получите их на https://my.telegram.org/")
        
        if not cls.PHONE:
            raise ValueError("PHONE обязателен!")
            
        if not cls.CHANNELS:
            raise ValueError("Укажите хотя бы один канал в CHANNELS!")
            
        if not cls.KEYWORDS:
            raise ValueError("Укажите хотя бы одно ключевое слово в KEYWORDS!")
        
        return True 
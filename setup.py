#!/usr/bin/env python3
"""
Скрипт быстрой настройки Telegram парсера
Помогает пользователю настроить конфигурацию
"""

import os
import sys


def create_env_file():
    """Создает .env файл с пользовательскими данными"""
    print("🚀 НАСТРОЙКА TELEGRAM ПАРСЕРА")
    print("=" * 50)
    
    # Проверяем существование .env файла
    if os.path.exists('.env'):
        overwrite = input("⚠️  Файл .env уже существует. Перезаписать? (y/n): ").strip().lower()
        if overwrite not in ['y', 'yes', 'да', 'д']:
            print("❌ Настройка отменена")
            return False
    
    print("\n📋 Введите необходимые данные:")
    print("💡 Получить API данные можно на https://my.telegram.org/")
    
    # Получаем данные от пользователя
    api_id = input("\n🔑 API ID: ").strip()
    api_hash = input("🔑 API Hash: ").strip()
    phone = input("📱 Номер телефона (с кодом страны, например +79123456789): ").strip()
    
    print("\n📺 Каналы для парсинга:")
    print("💡 Можно указывать @username или ID канала")
    print("💡 Для приватных каналов используйте ID (начинается с -100)")
    channels = input("📺 Каналы (через запятую): ").strip()
    
    print("\n🔍 Ключевые слова для поиска:")
    print("💡 Регистр не важен, можно на русском и английском")
    keywords = input("🔍 Ключевые слова (через запятую): ").strip()
    
    # Проверяем обязательные поля
    if not all([api_id, api_hash, phone, channels, keywords]):
        print("❌ Все поля обязательны для заполнения!")
        return False
    
    # Создаем .env файл
    env_content = f"""# Конфигурация Telegram парсера
# Сгенерировано автоматически {os.popen('date').read().strip()}

# API данные Telegram
API_ID={api_id}
API_HASH={api_hash}
PHONE={phone}

# Каналы для парсинга
CHANNELS={channels}

# Ключевые слова для поиска
KEYWORDS={keywords}
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("\n✅ Файл .env успешно создан!")
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка при создании файла: {e}")
        return False


def check_dependencies():
    """Проверяет установленные зависимости"""
    print("\n🔍 Проверка зависимостей...")
    
    try:
        import telethon
        import dotenv
        print("✅ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Не установлена зависимость: {e}")
        print("💡 Установите зависимости командой: pip install -r requirements.txt")
        return False


def main():
    """Основная функция настройки"""
    print("🎯 Добро пожаловать в настройку Telegram парсера!")
    
    # Проверяем зависимости
    if not check_dependencies():
        install = input("\n📦 Установить зависимости сейчас? (y/n): ").strip().lower()
        if install in ['y', 'yes', 'да', 'д']:
            os.system("pip install -r requirements.txt")
        else:
            print("❌ Сначала установите зависимости")
            return
    
    # Создаем конфигурацию
    if create_env_file():
        print("\n🎉 Настройка завершена!")
        print("\n📋 Что дальше:")
        print("1. 🚀 Запустите парсер: python main.py")
        print("2. ⚡ Или быстрый режим: python main.py --quick")
        print("3. 📖 Прочитайте README.md для подробной информации")
        
        # Предлагаем запустить парсер
        run_now = input("\n🚀 Запустить парсер сейчас? (y/n): ").strip().lower()
        if run_now in ['y', 'yes', 'да', 'д']:
            print("\n" + "="*50)
            os.system("python main.py")
    else:
        print("❌ Настройка не завершена")


if __name__ == "__main__":
    main() 
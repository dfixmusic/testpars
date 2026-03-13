#!/usr/bin/env python3
"""
Демонстрационный скрипт Telegram парсера
Показывает основные возможности без настройки
"""

import asyncio
from datetime import datetime


def print_demo_header():
    """Выводит заголовок демо"""
    print("🎯 DEMO - TELEGRAM ПАРСЕР")
    print("=" * 50)
    print("📋 Возможности парсера:")
    print("✅ Поиск постов по ключевым словам в ваших каналах")
    print("🌍 Глобальный поиск по всему Telegram")
    print("✅ Мониторинг в реальном времени")
    print("✅ Автоматическое сохранение с удобными именами")
    print("✅ Интерактивный интерфейс")
    print("=" * 50)


def show_sample_results():
    """Показывает пример результатов парсинга"""
    print("\n📊 ПРИМЕР РЕЗУЛЬТАТОВ ПАРСИНГА:")
    print("🔎 Ищу ключевые слова: bitcoin, криптовалюта, блокчейн")
    print("📺 Каналы: @bitcoin, @crypto_news, @blockchain_info")
    print("-" * 50)
    
    # Имитируем найденные посты
    sample_posts = [
        {
            'channel': '@bitcoin',
            'date': '2024-01-15 14:30:25',
            'keywords': ['bitcoin', 'price'],
            'views': 1250,
            'url': 'https://t.me/bitcoin/12345',
            'text': 'Bitcoin достиг нового максимума! Цена выросла на 15% за последние 24 часа...'
        },
        {
            'channel': '@crypto_news',
            'date': '2024-01-15 12:15:10',
            'keywords': ['блокчейн', 'технология'],
            'views': 890,
            'url': 'https://t.me/crypto_news/67890',
            'text': 'Новая блокчейн технология обещает революцию в финансовой сфере...'
        },
        {
            'channel': '@blockchain_info',
            'date': '2024-01-15 09:45:33',
            'keywords': ['криптовалюта', 'инвестиции'],
            'views': 2100,
            'url': 'https://t.me/blockchain_info/54321',
            'text': 'Аналитики прогнозируют рост криптовалют в следующем квартале...'
        }
    ]
    
    print(f"\n🎉 Найдено {len(sample_posts)} постов:")
    print("=" * 80)
    
    for i, post in enumerate(sample_posts, 1):
        print(f"\n📝 Пост #{i}")
        print(f"📍 Канал: {post['channel']}")
        print(f"📅 Дата: {post['date']}")
        print(f"🔑 Ключевые слова: {', '.join(post['keywords'])}")
        print(f"👀 Просмотры: {post['views']}")
        print(f"🔗 Ссылка: {post['url']}")
        print(f"💬 Текст: {post['text']}")
        print("-" * 40)


def show_setup_instructions():
    """Показывает инструкции по настройке"""
    print("\n🚀 КАК НАЧАТЬ ИСПОЛЬЗОВАТЬ:")
    print("=" * 50)
    
    print("\n1️⃣ Установите зависимости:")
    print("   pip install -r requirements.txt")
    
    print("\n2️⃣ Получите API данные:")
    print("   - Перейдите на https://my.telegram.org/")
    print("   - Создайте новое приложение")
    print("   - Скопируйте API ID и API Hash")
    
    print("\n3️⃣ Настройте конфигурацию:")
    print("   python setup.py")
    print("   # Или создайте .env файл вручную")
    
    print("\n4️⃣ Запустите парсер:")
    print("   python main.py")
    print("   # Или быстрый режим: python main.py --quick")


def show_features():
    """Показывает возможности парсера"""
    print("\n🔧 ВОЗМОЖНОСТИ ПАРСЕРА:")
    print("=" * 50)
    
    features = [
        "🔍 Поиск по ключевым словам в истории каналов",
        "🌍 Глобальный поиск по всему Telegram",
        "🔄 Мониторинг новых сообщений в реальном времени",
        "📊 Подробная информация о постах (дата, просмотры, ссылки)",
        "💾 Автоматическое сохранение с удобными именами файлов",
        "⚙️ Настройка лимитов и параметров поиска",
        "🎯 Поддержка публичных и приватных каналов",
        "🌐 Работа с русскими и английскими ключевыми словами",
        "📱 Интерактивный и понятный интерфейс"
    ]
    
    for feature in features:
        print(f"   {feature}")


def show_global_search_demo():
    """Показывает пример глобального поиска"""
    print("\n🌍 ПРИМЕР ГЛОБАЛЬНОГО ПОИСКА:")
    print("🔎 Поиск по всему Telegram: 'bitcoin'")
    print("📊 Лимит: 50 результатов")
    print("-" * 50)
    
    # Имитируем результаты глобального поиска
    global_posts = [
        {
            'source': '@crypto_world',
            'date': '2024-01-15 16:45:12',
            'keywords': ['bitcoin'],
            'views': 3400,
            'url': 'https://t.me/crypto_world/98765',
            'text': '🚀 Bitcoin breaks $50,000! This is just the beginning of the bull run...'
        },
        {
            'source': 'Crypto Traders Chat',
            'date': '2024-01-15 15:20:33',
            'keywords': ['bitcoin'],
            'views': 156,
            'url': None,
            'text': 'Guys, bitcoin is pumping hard! Who else is buying the dip?'
        },
        {
            'source': '@blockchain_daily',
            'date': '2024-01-15 14:10:45',
            'keywords': ['bitcoin'],
            'views': 2890,
            'url': 'https://t.me/blockchain_daily/54321',
            'text': 'Bitcoin network hashrate reaches all-time high. Network security stronger than ever!'
        }
    ]
    
    print(f"\n🎉 Найдено {len(global_posts)} постов из разных источников:")
    print("=" * 80)
    
    for i, post in enumerate(global_posts, 1):
        print(f"\n📝 Пост #{i}")
        print(f"📍 Источник: {post['source']}")
        print(f"📅 Дата: {post['date']}")
        print(f"🔑 Ключевые слова: {', '.join(post['keywords'])}")
        print(f"👀 Просмотры: {post['views']}")
        
        if post['url']:
            print(f"🔗 Ссылка: {post['url']}")
        
        print(f"💬 Текст: {post['text']}")
        print("-" * 40)
    
    print("\n💡 Преимущества глобального поиска:")
    print("   🌍 Поиск по всем публичным каналам Telegram")
    print("   🔍 Не нужно знать конкретные каналы")
    print("   📊 Больше результатов из разных источников") 
    print("   💾 Автоматическое сохранение результатов")


def show_examples():
    """Показывает примеры использования"""
    print("\n📝 ПРИМЕРЫ КОНФИГУРАЦИИ:")
    print("=" * 50)
    
    examples = [
        {
            'title': '💰 Криптовалютные новости',
            'channels': '@bitcoin,@ethereum,@crypto_news',
            'keywords': 'bitcoin,ethereum,price,bull,bear'
        },
        {
            'title': '💻 IT и программирование',
            'channels': '@tech_news,@programming,@python_news',
            'keywords': 'python,javascript,ai,разработка'
        },
        {
            'title': '📰 Общие новости',
            'channels': '@news_channel,@breaking_news',
            'keywords': 'новости,важно,срочно,breaking'
        }
    ]
    
    for example in examples:
        print(f"\n{example['title']}:")
        print(f"   CHANNELS={example['channels']}")
        print(f"   KEYWORDS={example['keywords']}")


async def simulate_real_time():
    """Имитирует мониторинг в реальном времени"""
    print("\n🔄 ДЕМО МОНИТОРИНГА В РЕАЛЬНОМ ВРЕМЕНИ:")
    print("=" * 50)
    print("⏳ Имитация работы мониторинга...")
    
    # Имитируем поступление новых сообщений
    new_messages = [
        "🆕 НОВЫЙ ПОСТ с ключевыми словами: bitcoin, price",
        "📍 Канал: @bitcoin_news",
        "💬 Текст: Bitcoin price surges to new all-time high...",
        "",
        "🆕 НОВЫЙ ПОСТ с ключевыми словами: блокчейн",
        "📍 Канал: @crypto_tech",
        "💬 Текст: Новая блокчейн платформа запущена..."
    ]
    
    for message in new_messages:
        print(message)
        await asyncio.sleep(1)
    
    print("\n✅ Демонстрация мониторинга завершена")


def main():
    """Основная функция демо"""
    print_demo_header()
    
    # Показываем меню демо
    while True:
        print("\n📋 ДЕМО МЕНЮ:")
        print("1. 📊 Показать пример результатов (поиск по каналам)")
        print("2. 🌍 Показать пример глобального поиска")
        print("3. 🔧 Показать возможности")
        print("4. 📝 Показать примеры конфигурации")
        print("5. 🔄 Демо мониторинга в реальном времени")
        print("6. 🚀 Инструкции по настройке")
        print("7. ❌ Выход")
        
        choice = input("\n👉 Ваш выбор (1-7): ").strip()
        
        if choice == "1":
            show_sample_results()
        elif choice == "2":
            show_global_search_demo()
        elif choice == "3":
            show_features()
        elif choice == "4":
            show_examples()
        elif choice == "5":
            asyncio.run(simulate_real_time())
        elif choice == "6":
            show_setup_instructions()
        elif choice == "7":
            print("\n👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    main() 
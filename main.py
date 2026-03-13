#!/usr/bin/env python3
"""
Главный файл для запуска Telegram парсера
Простой и быстрый поиск постов по ключевым словам
"""

import asyncio
import sys
from telegram_parser import TelegramParser


async def main():
    """Основная функция запуска парсера"""
    parser = TelegramParser()
    
    try:
        # Запуск и авторизация
        if not await parser.start():
            return
        
        print("\n" + "="*50)
        print("🎯 TELEGRAM ПАРСЕР ЗАПУЩЕН")
        print("="*50)
        
        # Показываем меню
        while True:
            print("\n📋 Выберите действие:")
            print("1. 🔍 Парсить каналы (поиск по истории)")
            print("2. 🌍 Глобальный поиск по всему Telegram")
            print("3. 🔄 Мониторинг в реальном времени")
            print("4. 📊 Показать последние результаты")
            print("5. 💾 Сохранить результаты в файл")
            print("6. ❌ Выход")
            
            choice = input("\n👉 Ваш выбор (1-6): ").strip()
            
            if choice == "1":
                # Парсинг истории каналов
                limit = input("📝 Количество сообщений для проверки в каждом канале (по умолчанию 100): ").strip()
                limit = int(limit) if limit.isdigit() else 100
                
                print(f"\n🚀 Начинаю парсинг с лимитом {limit} сообщений на канал...")
                posts = await parser.parse_all_channels(limit)
                
                if posts:
                    parser.print_results()
                    
                    # Автоматическое сохранение с удобным именем
                    filename = parser.save_to_file(search_type="channels")
                    print(f"💾 Результаты автоматически сохранены в: {filename}")
                else:
                    print("\n❌ Посты с указанными ключевыми словами не найдены")
            
            elif choice == "2":
                # Глобальный поиск по всему Telegram
                print("\n🔧 Настройка лимитов поиска:")
                lim = input("🔢 Максимум найденных постов (по умолчанию 50): ").strip()
                lim = int(lim) if lim.isdigit() and int(lim) > 0 else 50
                per_chat = input("🔢 Сообщений на канал/чат (по умолчанию 10): ").strip()
                per_chat = int(per_chat) if per_chat.isdigit() and int(per_chat) > 0 else 10
                
                # Передаем лимиты в интерактивный глобальный поиск
                await parser.interactive_global_search(global_limit=lim, per_chat_limit=per_chat)
            
            elif choice == "3":
                # Мониторинг в реальном времени
                await parser.setup_real_time_monitoring()
                print("\n🔄 Мониторинг запущен! Нажмите Ctrl+C для остановки...")
                
                try:
                    await parser.client.run_until_disconnected()
                except KeyboardInterrupt:
                    print("\n⏸️ Мониторинг остановлен")
            
            elif choice == "4":
                # Показать результаты
                if hasattr(parser, 'found_posts') and parser.found_posts:
                    # Определяем тип последних результатов
                    if 'source' in parser.found_posts[0]:
                        parser.print_global_results()
                    else:
                        parser.print_results()
                else:
                    print("❌ Нет результатов для отображения. Сначала выполните поиск.")
            
            elif choice == "5":
                # Сохранить в файл
                if hasattr(parser, 'found_posts') and parser.found_posts:
                    custom_name = input("📁 Введите имя файла (Enter для автоматического): ").strip()
                    if custom_name:
                        parser.save_to_file(filename=custom_name)
                    else:
                        # Определяем тип поиска для автоматического имени
                        search_type = "global_search" if 'source' in parser.found_posts[0] else "channels"
                        filename = parser.save_to_file(search_type=search_type)
                        print(f"💾 Результаты сохранены в: {filename}")
                else:
                    print("❌ Нет результатов для сохранения. Сначала выполните поиск.")
            
            elif choice == "6":
                # Выход
                print("👋 До свидания!")
                break
            
            else:
                print("❌ Неверный выбор, попробуйте снова")
    
    except KeyboardInterrupt:
        print("\n⏸️ Программа остановлена пользователем")
    
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
    
    finally:
        # Отключение от Telegram
        await parser.disconnect()


def run_quick_parse():
    """Быстрый запуск парсинга без меню (для продвинутых пользователей)"""
    async def quick_main():
        parser = TelegramParser()
        
        if await parser.start():
            print("🚀 Быстрый парсинг...")
            posts = await parser.parse_all_channels(50)  # Парсим по 50 сообщений
            parser.print_results()
            
            if posts:
                filename = parser.save_to_file(search_type="quick_channels")
                print(f"💾 Результаты сохранены в: {filename}")
            
            await parser.disconnect()
    
    asyncio.run(quick_main())


if __name__ == "__main__":
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Быстрый режим
        run_quick_parse()
    else:
        # Обычный режим с меню
        asyncio.run(main()) 
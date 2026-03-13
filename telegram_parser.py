import asyncio
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from telethon import TelegramClient, events
from telethon.tl.types import Message

from config import Config


class TelegramParser:
    """Основной класс для парсинга Telegram каналов"""
    
    def __init__(self):
        """Инициализация парсера"""
        Config.validate()
        
        self.client = TelegramClient(
            Config.SESSION_FILE,
            Config.API_ID, 
            Config.API_HASH
        )
        
        self.keywords = Config.KEYWORDS
        self.channels = Config.CHANNELS
        self.found_posts = []
        
    async def start(self):
        """Запуск клиента и авторизация"""
        print("🚀 Запуск Telegram парсера...")
        
        await self.client.start(phone=Config.PHONE)
        
        if await self.client.is_user_authorized():
            print("✅ Авторизация успешна!")
        else:
            print("❌ Ошибка авторизации")
            return False
            
        return True
    
    def _contains_keywords(self, text: str) -> List[str]:
        """Проверяет содержит ли текст ключевые слова"""
        if not text:
            return []
            
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in self.keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
                
        return found_keywords
    
    async def parse_channel_history(self, channel: str, limit: int = 100) -> List[Dict]:
        """Парсит историю сообщений канала"""
        print(f"🔍 Парсинг канала: {channel}")
        
        try:
            entity = await self.client.get_entity(channel)
            messages = []
            
            async for message in self.client.iter_messages(entity, limit=limit):
                if isinstance(message, Message) and message.text:
                    found_keywords = self._contains_keywords(message.text)
                    
                    if found_keywords:
                        post_data = {
                            'channel': channel,
                            'message_id': message.id,
                            'text': message.text,
                            'date': message.date,
                            'keywords': found_keywords,
                            'views': getattr(message, 'views', 0),
                            'url': f"https://t.me/{entity.username}/{message.id}" if entity.username else None
                        }
                        
                        messages.append(post_data)
                        print(f"✅ Найден пост с ключевыми словами: {', '.join(found_keywords)}")
            
            return messages
            
        except Exception as e:
            print(f"❌ Ошибка при парсинге канала {channel}: {e}")
            return []
    
    async def parse_all_channels(self, limit_per_channel: int = 100) -> List[Dict]:
        """Парсит все указанные каналы"""
        all_posts = []
        
        print(f"📊 Начинаю парсинг {len(self.channels)} каналов...")
        print(f"🔎 Ищу ключевые слова: {', '.join(self.keywords)}")
        
        for channel in self.channels:
            posts = await self.parse_channel_history(channel, limit_per_channel)
            all_posts.extend(posts)
            
            # Небольшая пауза между запросами
            await asyncio.sleep(1)
        
        # Сортируем по дате (новые сначала)
        all_posts.sort(key=lambda x: x['date'], reverse=True)
        
        self.found_posts = all_posts
        return all_posts
    
    def print_results(self):
        """Выводит результаты парсинга в консоль"""
        if not self.found_posts:
            print("\n❌ Посты с указанными ключевыми словами не найдены")
            return
            
        print(f"\n🎉 Найдено {len(self.found_posts)} постов:")
        print("=" * 80)
        
        for i, post in enumerate(self.found_posts, 1):
            print(f"\n📝 Пост #{i}")
            print(f"📍 Канал: {post['channel']}")
            print(f"📅 Дата: {post['date'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🔑 Ключевые слова: {', '.join(post['keywords'])}")
            print(f"👀 Просмотры: {post['views']}")
            
            if post['url']:
                print(f"🔗 Ссылка: {post['url']}")
            
            # Ограничиваем длину текста для вывода
            text_preview = post['text'][:200] + "..." if len(post['text']) > 200 else post['text']
            print(f"💬 Текст: {text_preview}")
            print("-" * 40)
    
    def save_to_file(self, filename: str = None, search_type: str = "channels"):
        """Сохраняет результаты в файл с автоматическим именем"""
        if not self.found_posts:
            print("❌ Нет данных для сохранения")
            return
        
        # Генерируем удобное имя файла если не указано
        if not filename:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            keywords_short = '_'.join(self.keywords[:3])  # Первые 3 ключевых слова
            filename = f"tg_parser_{search_type}_{keywords_short}_{timestamp}.txt"
            
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Результаты парсинга Telegram\n")
            f.write(f"Тип поиска: {search_type}\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Найдено постов: {len(self.found_posts)}\n")
            f.write(f"Ключевые слова: {', '.join(self.keywords)}\n")
            
            if search_type == "channels":
                f.write(f"Каналы: {', '.join(self.channels)}\n")
            else:
                f.write(f"Глобальный поиск по Telegram\n")
                
            f.write("=" * 80 + "\n\n")
            
            for i, post in enumerate(self.found_posts, 1):
                f.write(f"Пост #{i}\n")
                f.write(f"Источник: {post.get('channel', post.get('source', 'Неизвестно'))}\n")
                f.write(f"Дата: {post['date'].strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Ключевые слова: {', '.join(post['keywords'])}\n")
                f.write(f"Просмотры: {post.get('views', 0)}\n")
                
                if post.get('url'):
                    f.write(f"Ссылка: {post['url']}\n")
                
                f.write(f"Текст:\n{post['text']}\n")
                f.write("-" * 80 + "\n\n")
        
        print(f"💾 Результаты сохранены в файл: {filename}")
        return filename
    
    async def setup_real_time_monitoring(self):
        """Настройка мониторинга новых сообщений в реальном времени"""
        print("🔄 Настройка мониторинга в реальном времени...")

        # Приводим все каналы к username без @
        channel_usernames = set()
        for ch in self.channels:
            if isinstance(ch, str) and ch.startswith("@"):  # @username
                channel_usernames.add(ch[1:].lower())
            elif isinstance(ch, str):  # username
                channel_usernames.add(ch.lower())
            else:
                channel_usernames.add(str(ch))

        @self.client.on(events.NewMessage)
        async def handler(event):
            try:
                entity = await event.get_chat()
                username = getattr(entity, "username", None)
                channel_id = getattr(entity, "id", None)
                # Отладка: выводим информацию о чате
                print(f"[DEBUG] Получено сообщение из: username={username}, id={channel_id}")
                if username and username.lower() in channel_usernames:
                    if event.message.text:
                        found_keywords = self._contains_keywords(event.message.text)
                        if found_keywords:
                            print(f"\n🆕 НОВЫЙ ПОСТ с ключевыми словами: {', '.join(found_keywords)}")
                            print(f"📍 Канал: @{username}")
                            print(f"💬 Текст: {event.message.text[:100]}...")
                # Если нужно фильтровать по id, раскомментируйте:
                # elif str(channel_id) in channel_usernames:
                #     ...
            except Exception as e:
                print(f"⚠️ Ошибка в обработчике: {e}")

        print("✅ Мониторинг настроен! Бот будет уведомлять о новых постах с ключевыми словами")
        print("[INFO] Для работы мониторинга не забудьте вызвать client.run_until_disconnected() после setup_real_time_monitoring!")

# Пример запуска мониторинга:
# parser = TelegramParser()
# await parser.start()
# await parser.setup_real_time_monitoring()
# await parser.client.run_until_disconnected()  # Это важно!
    
    async def global_search(self, query: str, limit: int = 50, per_chat_limit: int = 10) -> List[Dict]:
        """Настоящий глобальный поиск по всему Telegram с расширяемыми лимитами"""
        print(f"🌍 Глобальный поиск по запросу: '{query}'")
        print(f"📊 Лимит результатов: {limit}, лимит сообщений на чат: {per_chat_limit}")
        
        found_posts = []
        
        try:
            from telethon.tl.functions.contacts import SearchRequest
            from telethon.tl.types import InputPeerEmpty
            
            print("🔍 Выполняю настоящий глобальный поиск...")
            
            # Используем поиск контактов для поиска публичных каналов/чатов
            try:
                contacts_result = await self.client(SearchRequest(
                    q=query,
                    limit=limit
                ))
                
                print(f"📨 Найдено {len(contacts_result.chats + contacts_result.users)} результатов поиска")
                
                # Проходим по найденным чатам/каналам
                for chat in contacts_result.chats:
                    try:
                        if hasattr(chat, 'username') or hasattr(chat, 'title'):
                            # Получаем последние сообщения из этого чата/канала
                            async for message in self.client.iter_messages(chat, limit=per_chat_limit):
                                if hasattr(message, 'message') and message.message:
                                    # Проверяем содержит ли сообщение наш запрос
                                    if query.lower() in message.message.lower():
                                        found_keywords = self._contains_keywords(message.message)
                                        
                                        source_info = getattr(chat, 'title', 'Неизвестный источник')
                                        if hasattr(chat, 'username') and chat.username:
                                            source_info = f"@{chat.username}"
                                        
                                        url = None
                                        if hasattr(chat, 'username') and chat.username:
                                            url = f"https://t.me/{chat.username}/{message.id}"
                                        
                                        post_data = {
                                            'source': source_info,
                                            'message_id': message.id,
                                            'text': message.message,
                                            'date': message.date,
                                            'keywords': found_keywords if found_keywords else [query.lower()],
                                            'views': getattr(message, 'views', 0),
                                            'url': url
                                        }
                                        
                                        found_posts.append(post_data)
                                        
                                        if len(found_posts) >= limit:
                                            break
                            
                            if len(found_posts) >= limit:
                                break
                                
                    except Exception:
                        # Пропускаем недоступные чаты
                        continue
                        
            except Exception as e:
                print(f"⚠️ Поиск контактов не удался: {e}")
            
            # Если мало результатов, пробуем альтернативный метод
            if len(found_posts) < 5:
                try:
                    print("🔄 Пробую альтернативный метод поиска...")
                    
                    # Используем поиск сообщений в диалогах
                    async for dialog in self.client.iter_dialogs(limit=100):
                        if dialog.is_channel or dialog.is_group:
                            try:
                                async for message in self.client.iter_messages(dialog.entity, limit=per_chat_limit):
                                    if hasattr(message, 'message') and message.message:
                                        if query.lower() in message.message.lower():
                                            found_keywords = self._contains_keywords(message.message)
                                            
                                            source_info = dialog.name or "Неизвестный источник"
                                            url = None
                                            
                                            if hasattr(dialog.entity, 'username') and dialog.entity.username:
                                                source_info = f"@{dialog.entity.username}"
                                                url = f"https://t.me/{dialog.entity.username}/{message.id}"
                                            
                                            post_data = {
                                                'source': source_info,
                                                'message_id': message.id,
                                                'text': message.message,
                                                'date': message.date,
                                                'keywords': found_keywords if found_keywords else [query.lower()],
                                                'views': getattr(message, 'views', 0),
                                                'url': url
                                            }
                                            
                                            found_posts.append(post_data)
                                            
                                            if len(found_posts) >= limit:
                                                break
                            except Exception:
                                continue
                                
                        if len(found_posts) >= limit:
                            break
                            
                except Exception as e:
                    print(f"⚠️ Альтернативный поиск не удался: {e}")
            
            print(f"✅ Найдено {len(found_posts)} постов с '{query}'")
            
        except Exception as e:
            print(f"❌ Ошибка при глобальном поиске: {e}")
            
        # Сортируем по дате (новые сначала)
        found_posts.sort(key=lambda x: x['date'], reverse=True)
        self.found_posts = found_posts
        
        return found_posts
    
    async def interactive_global_search(self, global_limit=50, per_chat_limit=10):
        """Интерактивный глобальный поиск с поддержкой лимитов"""
        print("\n🌍 ГЛОБАЛЬНЫЙ ПОИСК ПО TELEGRAM")
        print("=" * 50)
        print("💡 Этот режим ищет посты по всему Telegram, не только в ваших каналах")
        print("💡 Поиск работает по публичным каналам и группам")
        
        while True:
            print("\n📋 Выберите режим поиска:")
            print("1. 🔍 Поиск по одному ключевому слову")
            print("2. 🎯 Поиск по нескольким словам из конфига")
            print("3. 📝 Ввести новые ключевые слова")
            print("4. ⬅️ Вернуться в главное меню")
            
            choice = input("\n👉 Ваш выбор (1-4): ").strip()
            
            if choice == "1":
                query = input("\n🔍 Введите ключевое слово для поиска: ").strip()
                if not query:
                    print("❌ Ключевое слово не может быть пустым")
                    continue
                    
                print(f"\n🚀 Начинаю поиск '{query}'...")
                posts = await self.global_search(query, global_limit, per_chat_limit)
                
                if posts:
                    self.print_global_results()
                    
                    # Автоматическое сохранение
                    filename = self.save_to_file(search_type="global_search")
                    print(f"💾 Результаты автоматически сохранены в: {filename}")
                else:
                    print("❌ По вашему запросу ничего не найдено")
                    
            elif choice == "2":
                if not self.keywords:
                    print("❌ В конфигурации нет ключевых слов")
                    continue
                    
                print(f"🔍 Используем ключевые слова из конфига: {', '.join(self.keywords)}")
                
                all_posts = []
                
                for keyword in self.keywords[:3]:  # Ограничиваем первыми 3 словами
                    print(f"\n🔍 Поиск по слову: '{keyword}'")
                    posts = await self.global_search(keyword, global_limit // len(self.keywords[:3]), per_chat_limit)
                    all_posts.extend(posts)
                    
                    # Пауза между запросами
                    await asyncio.sleep(2)
                
                # Убираем дубликаты и сортируем
                seen = set()
                unique_posts = []
                for post in all_posts:
                    post_id = f"{post.get('source', '')}_{post['message_id']}"
                    if post_id not in seen:
                        seen.add(post_id)
                        unique_posts.append(post)
                
                self.found_posts = sorted(unique_posts, key=lambda x: x['date'], reverse=True)
                
                if self.found_posts:
                    self.print_global_results()
                    
                    # Автоматическое сохранение
                    filename = self.save_to_file(search_type="global_multi")
                    print(f"💾 Результаты автоматически сохранены в: {filename}")
                else:
                    print("❌ По вашим ключевым словам ничего не найдено")
                    
            elif choice == "3":
                new_keywords = input("\n🔍 Введите новые ключевые слова (через запятую): ").strip()
                if not new_keywords:
                    print("❌ Ключевые слова не могут быть пустыми")
                    continue
                    
                # Временно меняем ключевые слова
                old_keywords = self.keywords
                self.keywords = [kw.strip().lower() for kw in new_keywords.split(',') if kw.strip()]
                
                all_posts = []
                
                for keyword in self.keywords[:3]:  # Ограничиваем первыми 3 словами
                    print(f"\n🔍 Поиск по слову: '{keyword}'")
                    posts = await self.global_search(keyword, global_limit // len(self.keywords[:3]), per_chat_limit)
                    all_posts.extend(posts)
                    
                    # Пауза между запросами
                    await asyncio.sleep(2)
                
                # Убираем дубликаты и сортируем
                seen = set()
                unique_posts = []
                for post in all_posts:
                    post_id = f"{post.get('source', '')}_{post['message_id']}"
                    if post_id not in seen:
                        seen.add(post_id)
                        unique_posts.append(post)
                
                self.found_posts = sorted(unique_posts, key=lambda x: x['date'], reverse=True)
                
                if self.found_posts:
                    self.print_global_results()
                    
                    # Автоматическое сохранение
                    filename = self.save_to_file(search_type="global_custom")
                    print(f"💾 Результаты автоматически сохранены в: {filename}")
                else:
                    print("❌ По вашим ключевым словам ничего не найдено")
                
                # Возвращаем старые ключевые слова
                self.keywords = old_keywords
                    
            elif choice == "4":
                break
            else:
                print("❌ Неверный выбор, попробуйте снова")
    
    def print_global_results(self):
        """Выводит результаты глобального поиска"""
        if not self.found_posts:
            print("\n❌ Посты не найдены")
            return
            
        print(f"\n🎉 Найдено {len(self.found_posts)} постов:")
        print("=" * 80)
        
        for i, post in enumerate(self.found_posts, 1):
            print(f"\n📝 Пост #{i}")
            print(f"📍 Источник: {post.get('source', post.get('channel', 'Неизвестно'))}")
            print(f"📅 Дата: {post['date'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🔑 Ключевые слова: {', '.join(post['keywords'])}")
            print(f"👀 Просмотры: {post.get('views', 0)}")
            
            if post.get('url'):
                print(f"🔗 Ссылка: {post['url']}")
            
            # Ограничиваем длину текста для вывода
            text_preview = post['text'][:200] + "..." if len(post['text']) > 200 else post['text']
            print(f"💬 Текст: {text_preview}")
            print("-" * 40)

    async def disconnect(self):
        """Отключение от Telegram"""
        await self.client.disconnect()
        print("👋 Отключение от Telegram") 
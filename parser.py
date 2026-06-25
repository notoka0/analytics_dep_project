from telethon import TelegramClient
from telethon.tl.types import MessageEntityUrl, MessageEntityTextUrl
import asyncio, os
from database import init_db, save_post
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')

chat_username = 'ваш_чат'

async def main():
    init_db()

    async with TelegramClient('studrada_session', api_id, api_hash) as client:
        print("Триває підключення...")

        while True:
            print("Починається збір даних..")
            # Останні 100 постів
            async for message in client.iter_messages(chat_username, limit=100):
                # Ігнорування сервісних повідомлень
                if not message.text and not message.media:
                    continue

                post_id = message.id
                post_date = message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else ''
                char_count = len(message.text) if message.text else 0
                views = message.views if message.views else 0
                has_image = 1 if message.photo else 0
                has_link = 0 
                if message.entities:
                    for entity in message.entities:
                        if isinstance(entity, (MessageEntityUrl, MessageEntityTextUrl)):
                            has_link = 1
                            break

                target_reactions = {'👍': 0, '👎': 0, '🤬': 0, '🥰': 0, '😢': 0, '🤡': 0, '🔥': 0}

                if message.reactions:
                    for reaction_count in message.reactions.results:
                        if hasattr(reaction_count.reaction, 'emoticon'):
                            emoji = reaction_count.reaction.emoticon
                            if emoji in target_reactions:
                                target_reactions[emoji] = reaction_count.count
                
                # Зберігає id, дату, кількість символів, перегляди, наявність зображення, наявність посилання, поставлені реакції та їх кількість
                save_post(post_id, post_date, char_count, views, has_image, has_link, target_reactions)

            print("Базу даних оновлено.")
            print("Очікування 15 хвилин до наступного запуску...")
            await asyncio.sleep(900)

if __name__ == '__main__':
    asyncio.run(main())
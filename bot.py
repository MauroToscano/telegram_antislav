import logging
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, filters, Application
import re
import os
from datetime import datetime

def contains_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))

# Initialize the bot with your token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")


async def handle_message(update, context):
    message = update.message
    if message.chat.type not in ['group', 'supergroup']:
        return
    if message.from_user.id == context.bot.id:
        return
    if message.text and contains_cyrillic(message.text):
        try:
            # Delete the message first
            await message.delete()
            await context.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ban_info = f"[{timestamp}] Banned user {message.from_user.id} from chat {message.chat.id}\n"
            with open('banned_users.txt', 'a') as f:
                f.write(ban_info)
            logging.info(f"[{timestamp}] Deleted message and banned user {message.from_user.id} for using Cyrillic in chat {message.chat.id}")
        except Exception as e:
            logging.error(f"Failed to handle user {message.from_user.id} in chat {message.chat.id}: {e}")

async def handle_edited_message(update, context):
    message = update.edited_message
    if message.chat.type not in ['group', 'supergroup']:
        return
    if message.from_user.id == context.bot.id:
        return
    if message.text and contains_cyrillic(message.text):
        try:
            # Delete the message first
            await message.delete()
            await context.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ban_info = f"[{timestamp}] Banned user {message.from_user.id} from chat {message.chat.id}\n"
            with open('banned_users.txt', 'a') as f:
                f.write(ban_info)
            logging.info(f"[{timestamp}] Deleted edited message and banned user {message.from_user.id} for using Cyrillic in chat {message.chat.id}")
        except Exception as e:
            logging.error(f"Failed to handle user {message.from_user.id} in chat {message.chat.id}: {e}")

def main():
    application = Application.builder().token(TOKEN).build()
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.TEXT & filters.UpdateType.EDITED_MESSAGE, handle_edited_message))
    
    # Start the bot
    print("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bot stopped gracefully")

from telegram import Bot
from config import config

def send_notification_to_user(user_id, message):
    bot = Bot(token=config.BOT_TOKEN)
    bot.send_message(chat_id=user_id, text=message)

def send_notification_to_all_users(message):
    # This function assumes you have a list of all users or their IDs
    user_ids = [1, 2, 3]  # Example user IDs
    bot = Bot(token=config.BOT_TOKEN)
    for user_id in user_ids:
        bot.send_message(chat_id=user_id, text=message)

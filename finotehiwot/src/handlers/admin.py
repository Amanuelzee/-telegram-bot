from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from src.db.database import get_pending_users, approve_user, assign_car_and_registration_number

# Asynchronous function to approve users
async def approve(update: Update, context: CallbackContext):
    users = get_pending_users()
    if users:
        # Admin approves the first pending user
        user_id = users[0][0]  # User ID of the first pending user
        approve_user(user_id)
        assign_car_and_registration_number(user_id)
        await update.message.reply_text(f"User {users[0][1]} ምዝገባው ተረጋግጧል።")
    else:
        await update.message.reply_text("ማረጋገጫ የሚጠብቁ ምንም ተመዝጋቢ የለም!")

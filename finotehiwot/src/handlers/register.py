from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ConversationHandler,
)
from src.db.database import add_user

# Define the states for the conversation
FULL_NAME, PHONE_NUMBER, TELEGRAM_USERNAME, BANK_TRANSACTION_NUMBER = range(4)

# List of admin usernames
ADMINS = ["admin_username1", "admin_username2"]  # Replace with actual admin usernames

# Asynchronous function to handle the start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("እባኮትን ሙሉ ስምዎን ያስገቡ!")
    return FULL_NAME  # Transition to the FULL_NAME state

# Validation helper functions
def is_valid_phone_number(phone):
    return phone.isdigit() and 9 <= len(phone) <= 15

def is_valid_username(username):
    return username.startswith("@") and len(username) > 1

def is_valid_transaction_number(txn):
    return len(txn) >= 5  # Example condition

# Asynchronous function to handle user registration
async def register(update: Update, context: CallbackContext):
    user_data = context.user_data

    if "full_name" not in user_data:
        user_data["full_name"] = update.message.text
        await update.message.reply_text("እባክዎ የስልክ ቁጥርዎን ያስገቡ!")
        return PHONE_NUMBER

    elif "phone_number" not in user_data:
        if not is_valid_phone_number(update.message.text):
            await update.message.reply_text("የተሳሳተ የስልክ ቁጥር ነው። እባኮትን እንደገና ይሞክሩ።")
            return PHONE_NUMBER
        user_data["phone_number"] = update.message.text
        await update.message.reply_text("እባክዎ @ በማስቀደም የቴሌግራም መለያ ያስገቡ!")
        return TELEGRAM_USERNAME

    elif "telegram_username" not in user_data:
        username = update.message.text
        if not is_valid_username(username):
            username = f"@{update.message.from_user.username or update.message.from_user.id}"
        user_data["telegram_username"] = username
        await update.message.reply_text("በመጨረሻም የባንክ የገቢ ደረሰኝ ቁጥርን(transaction code) ያስገቡ!")
        return BANK_TRANSACTION_NUMBER

    elif "bank_transaction_number" not in user_data:
        if not is_valid_transaction_number(update.message.text):
            await update.message.reply_text("የተሳሳተ የግብይት ቁጥር ነው። እባኮትን እንደገና ይሞክሩ።")
            return BANK_TRANSACTION_NUMBER
        user_data["bank_transaction_number"] = update.message.text

        try:
            # Save user data to the database
            add_user(
                user_data["full_name"],
                user_data["phone_number"],
                user_data["telegram_username"],
                user_data["bank_transaction_number"],
            )
            await update.message.reply_text(
                "እናመሰግናለን! ምዝገባዎ ተሳክቷል። ይህንን መልዕክት በጥንቃቄ ያስቀምጡ።"
            )
        except Exception as e:
            await update.message.reply_text("ምዝገባውን ማስቀመጥ አልተቻለም። እባክዎ እንደገና ይሞክሩ።")
            print(f"Error saving user: {e}")

        return ConversationHandler.END  # End the conversation

# Asynchronous function to handle the cancel command
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("ሂደቱን ሰርዝ። እናመሰግናለን!")
    return ConversationHandler.END

# Admin command to view all registered users
async def view_users(update: Update, context: CallbackContext):
    if update.message.from_user.username not in ADMINS:
        await update.message.reply_text("ይህንን መረጃ ማየት አልተፈቀደልዎም።")
        return
    # Fetch and display users from the database
    users = []  # Fetch from the database if available
    if users:
        users_info = "\n".join(
            [f"Name: {u['name']}, Phone: {u['phone']}, Telegram: {u['username']}" for u in users]
        )
        await update.message.reply_text(f"Registered Users:\n\n{users_info}")
    else:
        await update.message.reply_text("ምዝገባ የተፈጠረ ተጠቃሚ የለም።")

# Admin command to add new admins
async def add_admin(update: Update, context: CallbackContext):
    if update.message.from_user.username not in ADMINS:
        await update.message.reply_text("ይህንን ትእዛዝ ማስፈጸም አልተፈቀደልዎም።")
        return

    new_admin = context.args[0] if context.args else None
    if new_admin and new_admin not in ADMINS:
        ADMINS.append(new_admin)
        await update.message.reply_text(f"{new_admin} አዲስ አስተዳዳሪ ተሰርቷል።")
    else:
        await update.message.reply_text("እባክዎ ትክክለኛ የተመለከተ መለያ ያስገቡ።")

# Main bot function
def main():
    application = Application.builder().token("7695126763:AAHiG9FJ0t8SQXBGrcYlvqaaFtT_P_7aLBc").build()

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register)],
            PHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, register)],
            TELEGRAM_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register)],
            BANK_TRANSACTION_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, register)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("view_users", view_users))
    application.add_handler(CommandHandler("add_admin", add_admin))

    application.run_polling()

if __name__ == "__main__":
    main()

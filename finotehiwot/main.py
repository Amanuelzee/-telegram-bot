from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackContext
import mysql.connector
from config.config import DB_CONFIG

# Check if DB_CONFIG is a dictionary
if isinstance(DB_CONFIG, dict):
    print("DB_CONFIG is a valid dictionary.")
else:
    print("Error: DB_CONFIG is not a dictionary.")

# Define the states
FULL_NAME, PHONE_NUMBER, TELEGRAM_USERNAME, BANK_TRANSACTION_NUMBER = range(4)

# List of admin usernames
ADMINS = ['mezekre_metsahft']

async def start(update: Update, context: CallbackContext):
    # Welcome message
    await update.message.reply_text(
        "👋 እንኳን ወደ ፍኖተ ብርሃን ሰ/ት/ቤት በደህና መጡ!\n"
        "📋 ለመመዝገብ እባክዎ ሙሉ ስምዎትን ያስገቡ።"
    )
    return FULL_NAME

async def register(update: Update, context: CallbackContext):
    user_data = context.user_data

    if update.message.text:
        if "full_name" not in user_data:
            user_data["full_name"] = update.message.text
            await update.message.reply_text(
                "✅ ሙሉ ስምዎ ተመዝግቦል።\n"
                "📞 እባክዎ ስልክ ቁጥዎን ያስገቡ።"
            )
            return PHONE_NUMBER
        elif "phone_number" not in user_data:
            phone_number = update.message.text
            # Validate phone number
            if not (phone_number.startswith("09") and len(phone_number) == 10 and phone_number.isdigit()):
                await update.message.reply_text(
                    "⚠️ ያስገቡት ቁጥር የተሳሳተ ነው። ስልክ ቁጥር በ09 የሚጀምር እና 8 ቁጥሮችን የያዘ መሆን አለበት።\n"
                    "እባክዎ በድጋሚ ያስገቡ።"
                )
                return PHONE_NUMBER
            user_data["phone_number"] = phone_number
            await update.message.reply_text(
                "📲 የስልክ ቁጥርዎ ተመዝግቦል።\n"
                "👤 እባክዎ የቴለግራም መጠቀሚያ ስምዎን @ን በማስቀደም ያስገቡ።"
            )
            return TELEGRAM_USERNAME
        elif "telegram_username" not in user_data:
            telegram_username = update.message.text
            # Validate Telegram username
            if not telegram_username.startswith("@") or len(telegram_username) < 4 or not telegram_username[1:].isalnum():
                await update.message.reply_text(
                    "⚠️ ያስገቡት የቴለግራም ስም የተሳሳተ ነው። የቴለግራም ስም @ እና በኋላ ከ3 የሚሆኑ ፊደላትና ቁጥሮች መያዝ አለበት።\n"
                    "እባክዎ በድጋሚ ያስገቡ።"
                )
                return TELEGRAM_USERNAME
            user_data["telegram_username"] = telegram_username
            await update.message.reply_text(
                "✔️ የቴለግራም መጠቀሚያ ስምዎ ተመዝግቦል።\n"
                "💳 እባክዎ የባንክ ደረሰኝ ቁጥር(transaction code) ያስገቡ።"
            )
            return BANK_TRANSACTION_NUMBER
        elif "bank_transaction_number" not in user_data:
            bank_transaction_number = update.message.text
            # Validate transaction number
            if not (bank_transaction_number.startswith("ft") and len(bank_transaction_number) == 12 and bank_transaction_number[2:].isalnum()):
                await update.message.reply_text(
                    "⚠️ ያስገቡት የባንክ ደረሰኝ ቁጥር የተሳሳተ ነው። በft የሚጀምር እና ከዚያ በኋላ 10 የሚሆኑ ቁጥሮችና ፊደላትን ያጠቃለለ ነው።\n"
                    "እባክዎ በድጋሚ ያስገቡ።"
                )
                return BANK_TRANSACTION_NUMBER
            user_data["bank_transaction_number"] = bank_transaction_number

            chat_id = update.message.from_user.id  # Get the user's chat ID
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()

                # Insert user data into the database
                cursor.execute("""
                INSERT INTO users (full_name, phone_number, telegram_username, bank_transaction_number, chat_id)
                VALUES (%s, %s, %s, %s, %s)
                """, (
                    user_data["full_name"],
                    user_data["phone_number"],
                    user_data["telegram_username"],
                    user_data["bank_transaction_number"],
                    chat_id,
                ))

                conn.commit()
                cursor.close()
                conn.close()

                await update.message.reply_text(
                    "🎉 እናመሰግናለን, ምዝገባዎ እየተከናወነ ነው። ምዝገባዎ ሲጠናቀቅ አጭር መልዕክት በቴሌግራም ይደርስዎታል! \n\n"
                    "📝 ያስገቡት መረጃ ከታች ተልክቷል:\n"
                    f"• **ሙሉ ሥም**: {user_data['full_name']}\n"
                    f"• **ቴለግራም መጠቀሚያ**: {user_data['telegram_username']}\n"
                    f"• **ስልክ ቁጥር**: {user_data['phone_number']}\n"
                    f"• **የባንክ ገቢ ደረሰኝ**: {user_data['bank_transaction_number']}\n\n"
                    "ቸር ይቆዩን!"
                )
            except mysql.connector.Error as err:
                await update.message.reply_text(f"⚠️ ችግር ነበር: {err}")

            return ConversationHandler.END


async def view_users(update: Update, context: CallbackContext):
    # Check if the user is an admin
    if update.message.from_user.username not in ADMINS:
        await update.message.reply_text("❌ ይቅርታ, ይህ ትእዛዝ ለአስተዳዳሪዎች ብቻ ነው።")
        return

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, full_name, phone_number, telegram_username, bank_transaction_number FROM users")
        users = cursor.fetchall()

        if not users:
            await update.message.reply_text("📋 እስካሁን የተመዘገቡ ተጠቃሚዎች የሉም።")
        else:
            user_list = "\n".join(
                [
                    f"ID: {user['id']}\n"
                    f"ሙሉ ስም: {user['full_name']}\n"
                    f"ስልክ: {user['phone_number']}\n"
                    f"ቴሌግራም: {user['telegram_username']}\n"
                    f"የባንክ ገቢ ቁጥር: {user['bank_transaction_number']}\n---"
                    for user in users
                ]
            )
            await update.message.reply_text(f"📋 የተመዘገቡ ተጠቃሚዎች:\n\n{user_list}")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        await update.message.reply_text(f"⚠️ ችግር ነበር: {err}")

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("❌ ምዝገባዎ ተሰርዟል።")
    return ConversationHandler.END

def main():
    TOKEN = "7695126763:AAHiG9FJ0t8SQXBGrcYlvqaaFtT_P_7aLBc"
    application = Application.builder().token(TOKEN).build()

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

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("view_users", view_users))  # Add the /view_users command

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from config import config
from src.handlers.start import start
from src.handlers.register import register
from src.handlers.admin import approve

async def main():
    # Initialize the bot with the token
    application = Application.builder().token(config.BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))

    # ConversationHandler for registration
    conversation_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, register)],
        states={
            'FULL_NAME': [MessageHandler(filters.TEXT, register)],
            'PHONE_NUMBER': [MessageHandler(filters.TEXT, register)],
            'TELEGRAM_USERNAME': [MessageHandler(filters.TEXT, register)],
            'BANK_TRANSACTION_NUMBER': [MessageHandler(filters.TEXT, register)],
        },
        fallbacks=[],
    )
    application.add_handler(conversation_handler)

    # Admin approval handler
    application.add_handler(CommandHandler("approve", approve))

    # Start the bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

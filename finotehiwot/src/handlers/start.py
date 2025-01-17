from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from src.db.database import add_user

async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    await update.message.reply_text(f"{user.first_name} እንኳን በደህና መጡ! ቀጥሎ የሚጠየቁትን በመሙላት ለጉዞ ይመዝገቡ።")
    
    # Ask for user details
    await update.message.reply_text("እባክዎ ሙሉ ስምዎን ያስገቡ!")
    return 'FULL_NAME'  # Transition to the next state


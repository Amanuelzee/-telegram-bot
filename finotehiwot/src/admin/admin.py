from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from src.db.database import get_pending_users, approve_user, assign_registration_id, send_approval_notification
import json

# Fetch pending users from the database
async def view_registered_users(update: Update, context: CallbackContext):
    users = get_pending_users()  # Fetch pending users from the database
    if not users:
        await update.message.reply_text("No pending users for approval.")
    else:
        user_list = "\n".join([f"ID: {user[0]} | Name: {user[1]}" for user in users])
        await update.message.reply_text(f"Pending Users:\n{user_list}")

# Approve a user after certain criteria
async def approve(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Please provide the user ID to approve.")
        return

    user_id = context.args[0]  # Get user ID from the command
    users = get_pending_users()

    # Find the user to approve
    user_to_approve = next((user for user in users if str(user[0]) == user_id), None)
    if not user_to_approve:
        await update.message.reply_text(f"User with ID {user_id} not found.")
        return

    # Criteria for approval (e.g., transaction number)
    # You can modify this according to your criteria
    if approve_user(user_id):
        registration_id = assign_registration_id(user_id)
        send_approval_notification(user_to_approve[1], registration_id)  # Send Telegram notification
        await update.message.reply_text(f"User {user_to_approve[1]} has been approved. Registration ID: {registration_id}")
    else:
        await update.message.reply_text(f"User {user_to_approve[1]} failed the approval criteria.")

# Export approved user data into a file
async def export_approved_user(update: Update, context: CallbackContext):
    users = get_pending_users()
    approved_users = [user for user in users if user[4] == 'approved']  # Filter by approved users
    if approved_users:
        filename = "approved_users.json"
        with open(filename, 'w') as file:
            json.dump(approved_users, file, indent=4)
        await update.message.reply_text(f"Approved users data exported to {filename}.")
    else:
        await update.message.reply_text("No approved users to export.")

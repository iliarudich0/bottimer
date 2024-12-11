import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# ✅ Get the token from the environment variable (set in Railway)
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    raise ValueError("⚠️ Environment variable 'TOKEN' is not set. Please set it in Railway or locally.")

# ✅ Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ✅ Function to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message when the bot is started."""
    logging.info(f"User {update.effective_user.id} started the bot.")
    await update.message.reply_text('👋 Hi! I am a bot that sends scheduled messages. Use /set_timer to start hourly messages.')

# ✅ Function to send a scheduled message
async def send_scheduled_message(context: CallbackContext) -> None:
    """Sends the scheduled message to the user."""
    try:
        chat_id = context.job.context
        message = "⏰ This is a scheduled message."
        logging.info(f"Sending scheduled message to chat_id={chat_id}")
        await context.bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logging.error(f"❌ Failed to send a scheduled message: {e}")

# ✅ Command to set up the timer
async def set_timer(update: Update, context: CallbackContext) -> None:
    """Sets up a repeating job to send messages every hour."""
    try:
        # Get the chat ID of the user
        chat_id = update.message.chat_id

        # Remove existing jobs for this user to avoid multiple timers
        existing_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        if existing_jobs:
            for job in existing_jobs:
                job.schedule_removal()
                logging.info(f"✅ Removed existing job for chat_id={chat_id}")

        # Set up a repeating job (every hour)
        context.job_queue.run_repeating(
            send_scheduled_message, 
            interval=3600,  # 1 hour = 3600 seconds
            first=0,  # Send the first message immediately
            context=chat_id,
            name=str(chat_id)
        )

        logging.info(f"✅ Timer set for chat_id={chat_id}")
        await update.message.reply_text('⏳ Timer is set! I will send messages every hour.')
    except Exception as e:
        logging.error(f"❌ Error while setting timer: {e}")
        await update.message.reply_text(f'⚠️ An error occurred while setting the timer: {e}')

# ✅ Build the application and add command handlers
application = Application.builder().token(TOKEN).build()

# Add commands to the bot
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('set_timer', set_timer))

if __name__ == "__main__":
    logging.info("🚀 Bot is starting...")
    application.run_polling()

import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler

# Get the token from the environment variable (set in Railway)
TOKEN = os.getenv('TOKEN')

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Function to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! I am a bot that sends scheduled messages.')

# Function to send a scheduled message
async def send_scheduled_message(context: CallbackContext) -> None:
    chat_id = context.job.context
    message = "This is a scheduled message ⏰"
    await context.bot.send_message(chat_id=chat_id, text=message)

# Command to set up the timer
async def set_timer(update: Update, context: CallbackContext) -> None:
    try:
        # Set up a repeating job (every hour)
        context.job_queue.run_repeating(send_scheduled_message, interval=3600, context=update.message.chat_id)
        await update.message.reply_text('Timer is set! I will send messages every hour.')
    except Exception as e:
        await update.message.reply_text(f'An error occurred: {e}')

# Main function to run the bot
async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Commands for the bot
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('set_timer', set_timer))

    # Start polling for updates
    await application.run_polling()

if __name__ == "__main__":
    application.run_polling()

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
from Dialogflow import PRJ_ID, TELEGRAM_ID, LANGUAGE_CODE, detect_intent_texts

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    # 1/0
    """Send a message when the command /start is issued."""
    # update.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
    # update.message.reply_text('Hi!')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi!")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def get_answer(update, context):
    """Echo the user message."""
    text = update.message.text
    answer, intent_name, confidence, is_fallback = detect_intent_texts(
        project_id=PRJ_ID,
        session_id=TELEGRAM_ID,
        text=text,
        language_code=LANGUAGE_CODE
        )

    update.message.reply_text(answer)


def error(update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, get_answer))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
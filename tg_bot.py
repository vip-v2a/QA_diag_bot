from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
from dotenv import load_dotenv
from Dialogflow import PRJ_ID, TELEGRAM_ID, LANGUAGE_CODE, detect_intent_texts
from bots_logger import TelegramLogsHandler, TG_STRFMT

logger = logging.getLogger(__file__)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi!")


def help(update, context):
    update.message.reply_text(
        "The chatbot answers the most frequent questions"
    )


def get_answer(update, context):
    text = update.message.text
    answer, intent_name, confidence, is_fallback = detect_intent_texts(
        project_id=PRJ_ID,
        session_id=TELEGRAM_ID,
        text=text,
        language_code=LANGUAGE_CODE
    )

    update.message.reply_text(answer)


def error(update, error):
    logger.warning("Update '%s' caused error '%s'", update, error)


def main():

    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    tg_handler = TelegramLogsHandler(
        bot_token=bot_token,
        chat_id=TELEGRAM_ID,
        fmt=TG_STRFMT
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(tg_handler)
    logger.info("tg-bot started")

    updater = Updater(token=bot_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, get_answer))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

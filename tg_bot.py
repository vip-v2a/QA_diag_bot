from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
from Dialogflow import PRJ_ID, TELEGRAM_ID, LANGUAGE_CODE, detect_intent_texts
from dotenv import load_dotenv


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
    logging.warning("Update '%s' caused error '%s'", update, error)


def main():

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    updater = Updater(token=bot_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, get_answer))

    dp.add_error_handler(error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()

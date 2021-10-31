import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import os
import time
from dotenv import load_dotenv
import logging
from Dialogflow import PRJ_ID, TELEGRAM_ID, LANGUAGE_CODE, detect_intent_texts
from bots_logger import TelegramLogsHandler, VK_STRFMT

logger = logging.getLogger(__file__)


def get_answer_dialogflow(event, vk, _user_id):

    text = event.obj.text

    answer, intent_name, confidence, is_fallback = detect_intent_texts(
        project_id=PRJ_ID,
        session_id=_user_id,
        text=text,
        language_code=LANGUAGE_CODE
    )

    if not is_fallback:
        vk.messages.send(
            user_id=event.obj.peer_id,
            message=answer,
            random_id=int(time.time())
        )


def echo(event, vk):
    vk.messages.send(
        user_id=event.obj.peer_id,
        message=event.obj.text,
        random_id=int(time.time())
    )


def main():

    load_dotenv()
    vk_token = os.getenv("VK_TOKEN")
    vk_bot_id = os.getenv("VK_BOT_ID")
    bot_token = os.getenv("BOT_TOKEN")

    tg_handler = TelegramLogsHandler(
        bot_token=bot_token,
        chat_id=TELEGRAM_ID,
        fmt=VK_STRFMT
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(tg_handler)
    logger.info("vk-bot started")

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, vk_bot_id)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:

            vk_user_id = event.obj.from_id
            get_answer_dialogflow(event, vk, vk_user_id)
            logger.debug(
                "Новое сообщение: \nДля меня от:"
                f"{vk_user_id}\nТекст: {event.obj.text}"
            )

        elif event.type == VkBotEventType.MESSAGE_REPLY:
            logger.debug(
                "Новое сообщение: \nОт меня для: "
                f"{event.obj.peer_id}\nТекст: {event.obj.text}\n"
            )

        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            logger.debug(
                f"Печатает {event.obj.from_id} для {event.obj.to_id}\n"
            )

        elif event.type == VkBotEventType.GROUP_JOIN:
            logger.debug(
                f"Вступил в группу {event.obj.user_id}"
            )

        elif event.type == VkBotEventType.GROUP_LEAVE:
            logger.debug(
                f"Покинул группу {event.obj.user_id}"
            )

        else:
            logger.info(f"{event.type}")

if __name__ == "__main__":
    main()

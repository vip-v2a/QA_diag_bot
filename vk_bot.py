import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import os
import time
from Dialogflow import PRJ_ID, TELEGRAM_ID, LANGUAGE_CODE, detect_intent_texts
from dotenv import load_dotenv
import logging


def get_answer_dialogflow(event, vk):

    text = event.obj.text

    answer, intent_name, confidence, is_fallback = detect_intent_texts(
        project_id=PRJ_ID,
        session_id=TELEGRAM_ID,
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

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

    load_dotenv()
    vk_token = os.getenv("VK_TOKEN")
    vk_bot_id = os.getenv("VK_BOT_ID")

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, vk_bot_id)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:

            get_answer_dialogflow(event, vk)
            logging.info(
                "Новое сообщение: \nДля меня от:"
                f"{event.obj.from_id}\nТекст: {event.obj.text}"
            )

        elif event.type == VkBotEventType.MESSAGE_REPLY:
            logging.info(
                "Новое сообщение: \nОт меня для: "
                f"{event.obj.peer_id}\nТекст: {event.obj.text}\n"
            )

        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            logging.info(
                f"Печатает {event.obj.from_id} для {event.obj.to_id}\n"
            )

        elif event.type == VkBotEventType.GROUP_JOIN:
            logging.info(
                f"Вступил в группу {event.obj.user_id}"
            )

        elif event.type == VkBotEventType.GROUP_LEAVE:
            logging.info(
                f"Покинул группу {event.obj.user_id}"
            )

        else:
            logging.info(f"{event.type}")

if __name__ == "__main__":
    main()

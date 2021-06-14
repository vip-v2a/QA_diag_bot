# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import os
import time
from Dialogflow import PRJ_ID, TELEGRAM_ID, LANGUAGE_CODE, detect_intent_texts

VK_TOKEN = os.getenv("VK_TOKEN")
# TODO: убрать в локальную переменную


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
    """ Пример использования bots longpoll

        https://vk.com/dev/bots_longpoll
    """
    vk_bot_id = os.getenv('VK_BOT_ID')

    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, vk_bot_id)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            
            get_answer_dialogflow(event, vk)

            print('Новое сообщение:')
            print('Для меня от: ', end='')
            print(event.obj.from_id)
            print('Текст:', event.obj.text)
            print()

        elif event.type == VkBotEventType.MESSAGE_REPLY:
            print('Новое сообщение:')

            print('От меня для: ', end='')

            print(event.obj.peer_id)

            print('Текст:', event.obj.text)
            print()

        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            print('Печатает ', end='')

            print(event.obj.from_id, end=' ')

            print('для ', end='')

            print(event.obj.to_id)
            print()

        elif event.type == VkBotEventType.GROUP_JOIN:
            print(event.obj.user_id, end=' ')

            print('Вступил в группу!')
            print()

        elif event.type == VkBotEventType.GROUP_LEAVE:
            print(event.obj.user_id, end=' ')

            print('Покинул группу!')
            print()

        else:
            print(event.type)
            print()


if __name__ == '__main__':
    main()
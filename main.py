# -*- coding: utf-8 -*-
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from mtok import tel, pas, token


def main():

    vk_session = vk_api.VkApi(login=tel, password=pas, token=token)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')

            if event.from_me:
                print('От меня для: ', end='')
            elif event.to_me:
                print('Для меня от: ', end='')

            if event.from_user:
                print(event.user_id)
            elif event.from_chat:
                print(event.user_id, 'в беседе', event.chat_id)
            elif event.from_group:
                print('группы', event.group_id)

            print('Текст: ', event.text)
            print()

        elif event.type == VkEventType.USER_TYPING:
            print('Печатает ', end='')

            if event.from_user:
                print(event.user_id)
            elif event.from_group:
                print('администратор группы', event.group_id)

        elif event.type == VkEventType.USER_TYPING_IN_CHAT:
            print('Печатает ', event.user_id, 'в беседе', event.chat_id)

        elif event.type == VkEventType.USER_ONLINE:
            print('Пользователь', event.user_id, 'онлайн', event.platform)

        elif event.type == VkEventType.USER_OFFLINE:
            print('Пользователь', event.user_id, 'оффлайн', event.offline_type)

        else:
            print(event.type, event.raw[1:])


if __name__ == '__main__':
    main()

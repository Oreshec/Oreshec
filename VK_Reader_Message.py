import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import time
import traceback

# Token file
from config import token

# authorization
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


# definition is it a person or a bot by ID
def user_detector(event):
    try:
        if event.user_id > 0:
            user = vk.users.get(user_ids=event.user_id)  # Получаем информацию о пользователе
            user_name = user[0]['first_name']  # Имя
            user_last_name = user[0]['last_name']  # Фамилия
            user_id = str(user[0]['id'])  # ID
            user_info = user_name + ' ' + user_last_name + " " + user_id  # Все вместе
            print(f'{user_info}')
        elif event.user_id < 0:
            print(f'Бот №{event.user_id*-1}')  # Те у кого -ID просто крашат код и не дают информацию

    except AttributeError:
        print(f'Бот №{event.peer_id*-1}')
    except ExceptionGroup:
        print('Я хз че это значит', f'"{traceback.format_exc()}"')


# Получаем информацию о Беседе
def chat_conversation(chat_id):
    chat = vk.messages.getChat(chat_id=chat_id)  # Даем запрос об информации о беседе
    chat_title = chat["title"]  # Название беседы
    chat_id = str(chat["id"])  # ID беседы
    chat_info = chat_title + ' ' + chat_id  # Все вместе
    print(chat_info)


def group_detector(event):
    try:
        group_id = event.group_id
        group = vk.groups.getAddresses(group_id=group_id)
        group_title = group[0]['title']
        print(group_title)
    except KeyError:
        print(f'Группа №{event.group_id}')


def main():
    print("Worked")
    print()

    for event in longpoll.listen():  # Запускаем процесс "прослушки"

        if event.type == VkEventType.MESSAGE_NEW:  # Проверяем на условие нового сообщения

            print('New Message!')
            print(time.asctime())

            if event.from_me:
                print('From me for:', end=' ')
                user_detector(event)
            elif event.to_me:
                print('For me from:', end=' ')
                user_detector(event)
            elif event.from_user:
                print('From the user:', end=' ')
                user_detector(event)

            if event.from_chat:
                print('in chat:', end=' ')
                chat_conversation(event.chat_id)
            elif event.from_group:
                print('groups:', end=' ')
                group_detector(event)
            print('Text:', event.text, ' ')
            print()

            # the user types a message
        if event.type == VkEventType.USER_TYPING:
            print(time.asctime(), end=' ')
            user_detector(event)
            print('Typing... ')
            if event.from_user:
                print(event.user_id)
                user_detector(event)
            elif event.from_group:
                print('Group Administrator', event.group_id)
        if event.type == VkEventType.USER_TYPING_IN_CHAT:
            print(time.asctime())
            print('Typing ')
            user_detector(event)
            print('in chat', end=' ')
            chat_conversation(event.chat_id)

        if event.type == VkEventType.USER_ONLINE:
            print(time.asctime())
            print('User')
            user_detector(event)
            print('online', event.platform)
        if event.type == VkEventType.USER_OFFLINE:
            print(time.asctime())
            print('User')
            user_detector(event)
            print('offline', event.offline_type)


if __name__ == '__main__':
    main()

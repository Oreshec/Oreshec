import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import time
import sqlite3
import traceback

# Token file
from config import main_token

# Base Data
db = sqlite3.connect('base.db')
# Cursor
c = db.cursor()
# Create table
c.execute("""CREATE TABLE IF NOT EXISTS Event_text (
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_vk_id INTEGER,
first_name TEXT,
last_name TEXT,
message TEXT,
chat_title TEXT,
chat_id TEXT,

time TEXT
)""")

# authorization
vk_session = vk_api.VkApi(token=main_token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


# definition is it a person or a bot by ID
def detector(peer_id=0, user_id=0):
    if user_id > 0:
        user = vk.users.get(user_ids=user_id)  # Получаем информацию о пользователе
        first_name = user[0]['first_name']  # Имя
        last_name = user[0]['last_name']  # Фамилия
        user_id = user[0]['id']  # ID
        # user_info = first_name + ' ' + last_name + " " + str(user_id)  # Все вместе
        # print(user_info)
        if peer_id > 2000000000:
            peer_id = peer_id - 2000000000
            chat = vk.messages.getChat(chat_id=peer_id)  # Даем запрос об информации о беседе
            chat_title = str(chat["title"])  # Название беседы
            chat_id = str(chat["id"])  # ID беседы
            # chat_info = chat_title + ' ' + chat_id  # Все вместе
            # print(chat_info)
            return user_id, first_name, last_name, chat_title, chat_id
        else:
            return user_id, first_name, last_name
    elif user_id < 0:
        if peer_id > 2000000000:
            peer_id = peer_id - 2000000000
            chat = vk.messages.getChat(chat_id=peer_id)  # Даем запрос об информации о беседе
            chat_title = str(chat["title"])  # Название беседы
            chat_id = str(chat["id"])  # ID беседы
            # chat_info = chat_title + ' ' + chat_id  # Все вместе
            # print(chat_info)
            return "Unknown", "Unknown", "Unknown", chat_title, chat_id
        else:
            return "Unknown", "Unknown", "Unknown"

    if peer_id > 2000000000:
        peer_id = peer_id - 2000000000
        chat = vk.messages.getChat(chat_id=peer_id)  # Даем запрос об информации о беседе
        chat_title = str(chat["title"])  # Название беседы
        chat_id = str(chat["id"])  # ID беседы
        # chat_info = chat_title + ' ' + chat_id  # Все вместе
        # print(chat_info)
        return chat_title, chat_id
    elif peer_id < 2000000000:
        return "Unknown", "Unknown", "Unknown"

    if peer_id == user_id:
        if user_id == 0:
            print('Error 0')
            return False
    else:
        return "Unknown", "Unknown", "Unknown"


def write(user_id, first_name, last_name, chat_title=' ', chat_id=' ', message=' '):
    c.execute(
        f"""INSERT OR IGNORE INTO Event_text 
        (user_vk_id, first_name, last_name, time, chat_title, chat_id,  message) VALUES(?, ?, ?, ?, ?, ?, ?)""",
        (user_id, first_name, last_name, time.asctime(), chat_title, chat_id, message))
    db.commit()


def main():
    while True:
        try:
            print("Worked\n\n")
            for event in longpoll.listen():  # Запускаем процесс "прослушки"

                if event.type == VkEventType.MESSAGE_NEW:  # Проверяем на условие нового сообщения

                    print('\nNew Message!')
                    print(time.asctime())

                    if event.from_me:
                        print('From me for:', end=' ')
                    elif event.to_me:
                        print('For me from:', end=' ')
                    elif event.from_user:
                        print('From the user:', end=' ')
                    print(detector(user_id=event.user_id))

                    if event.from_chat:
                        print('in chat', end=" ")
                        print(detector(event.peer_id))
                    elif event.from_group:
                        print('groups', event.group_id)
                    print(f'Text: {event.text}')

                    write(*detector(peer_id=event.peer_id, user_id=event.user_id), message=event.text)

                    # the user types a message
                if event.type == VkEventType.USER_TYPING:
                    print(time.asctime(), end=' ')
                    detector(event.peer_id, event.user_id)
                    print('Typing... ')
                    if event.from_user:
                        print(event.user_id)
                        detector(event.peer_id, event.user_id)
                    elif event.from_group:
                        print('Group Administrator', event.group_id)
                if event.type == VkEventType.USER_TYPING_IN_CHAT:
                    print(time.asctime())
                    print('Typing ')
                    detector(event.peer_id, event.user_id)
                    print('in chat', end=" ")
                    detector(event.peer_id, event.user_id)

                if event.type == VkEventType.USER_ONLINE:
                    print(time.asctime())
                    print('User')
                    detector(event.peer_id, event.user_id)
                    print('online', event.platform)
                if event.type == VkEventType.USER_OFFLINE:
                    print(time.asctime())
                    print('User')
                    detector(event.peer_id, event.user_id)
                    print('offline', event.offline_type)

        except Exception:
            print(traceback.format_exc())
            for i in range(1, 11):
                time.sleep(1)
                print(f'{i}/10')
            pass


if __name__ == '__main__':
    main()

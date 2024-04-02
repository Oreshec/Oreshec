import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import time
import traceback
import asyncio

# Token file
from config import main_token


# definition is it a person or a bot by ID
async def user_detector(event, vk):
    try:
        if event.user_id > 0:
            user = vk.users.get(user_ids=event.user_id)  # Получаем информацию о пользователе
            user_info = user[0]['first_name'] + " " + user[0]['last_name'] + " " + str(user[0]['id'])
            print(f'{user_info}')
        else:
            print(f'Бот №{event.user_id * -1}')  # Те у кого -ID просто крашат код и не дают информацию

    except AttributeError:
        print(f'Бот №{event.peer_id * -1}')
    except ExceptionGroup:
        print('Я хз че это значит', f'"{traceback.format_exc()}"')


# Получаем информацию о Беседе
async def chat_conversation(chat_id, vk):
    chat = vk.messages.getChat(chat_id=chat_id)  # Даем запрос об информации о беседе
    chat_title = chat["title"]  # Название беседы
    chat_id = str(chat["id"])  # ID беседы
    chat_info = chat_title + ' ' + chat_id  # Все вместе
    print(chat_info)


async def group_detector(event, vk):
    try:
        group_id = event.group_id
        group = vk.groups.getAddresses(group_id=group_id)
        group_title = group[0]['title']
        print(group_title)
    except KeyError:
        print(f'Группа №{event.group_id}')


async def read():
    try:
        vk_session = vk_api.VkApi(token=main_token)
        longpoll = VkLongPoll(vk_session)
        vk = vk_session.get_api()

        print(f"Worked")

        for event in longpoll.listen():  # Запускаем процесс "прослушки"

            if event.type == VkEventType.MESSAGE_NEW:  # Проверяем на условие нового сообщения
                print('New Message!')
                print(time.asctime())

                if event.from_me:
                    print('From me for:', end=' ')
                elif event.to_me:
                    print('For me from:', end=' ')
                elif event.from_user:
                    print('From the user:', end=' ')
                await user_detector(event, vk)

                if event.from_chat:
                    print('in chat:', end=' ')
                    await chat_conversation(event.chat_id, vk)
                elif event.from_group:
                    print('groups:', end=' ')
                    await group_detector(event, vk)

                if event.text != "":
                    print('Text:', event.text, ' ')
                    print()
                else:
                    print(f'Нет текста!\n')

                    # the user types a message
                if event.type == VkEventType.USER_TYPING:
                    print(time.asctime(), end=' ')
                    await user_detector(event, vk)
                    print('Typing... ')
                    if event.from_user:
                        print(event.user_id)
                        await user_detector(event, vk)
                    elif event.from_group:
                        print('Group Administrator', event.group_id)
                if event.type == VkEventType.USER_TYPING_IN_CHAT:
                    print(time.asctime())
                    print('Typing ')
                    await user_detector(event, vk)
                    print('in chat', end=' ')
                    await chat_conversation(event.chat_id, vk)

                if event.type == VkEventType.USER_ONLINE:
                    print(time.asctime())
                    print('User')
                    await user_detector(event, vk)
                    print('online', event.platform)
                if event.type == VkEventType.USER_OFFLINE:
                    print(time.asctime())
                    print('User')
                    await user_detector(event, vk)
                    print('offline', event.offline_type)
    except Exception as e:
        print(e)
        asyncio.run(read())


if __name__ == '__main__':
    asyncio.run(read())

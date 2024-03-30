import vk_api
import traceback

from config import main_token

session = vk_api.VkApi(token=main_token)
vk = session.get_api()


def group_chat_get_user_info():
    try:
        while True:
            chat_id = input('Введите ID чата: ')
            if chat_id == "Exit":
                break
            else:
                chat = vk.messages.getChat(chat_id=chat_id)
                chat_title = chat["title"]
                chat_id = chat["id"]
                chat_users = chat["users"]
                print('Title: ', chat_title)
                print('ID: ', chat_id)

                n = len(chat_users)
                l = 0
                b = 0
                while l < n:
                    if chat_users[l] > 0:
                        user = vk.users.get(user_ids=chat_users)
                        print(l + 1)
                        print(user[l]['first_name'] + ' ' + user[l]['last_name'])
                        print(user[l]['id'])
                        l = l + 1
                    elif chat_users[l] < 0:
                        n = n - 1
                        l = l + 1
                        b = b + 1
                print(b)
                print('Done')
    except vk_api.exceptions.ApiError:
        print(f'Диалога {chat_id} не существует!')
        group_chat_get_user_info()

if __name__ == '__main__':
    group_chat_get_user_info()

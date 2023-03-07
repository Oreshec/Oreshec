import vk_api

from key import main_token

session = vk_api.VkApi(token=main_token)
vk = session.get_api()


def group_chat_get_user_info():
    chat_id = input('Введите ID чата ')

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


if __name__ == '__main__':
    group_chat_get_user_info()

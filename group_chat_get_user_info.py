import vk_api

from config import main_token

def enumeration(user, chat_users):
    try:
        for i in range(len(chat_users)):
            print(f'№{i+1}')
            print('\tName: ', user[i]['first_name'] + ' ' + user[i]['last_name'])
            print('\tID: ' ,user[i]['id'])
    except IndexError as e:
        print('Error',e)
        pass

def group_chat_get_user_info():
    session = vk_api.VkApi(token=main_token)
    vk = session.get_api()
    try:
        while True:
            chat_id = input('Введите ID чата: ')
            if chat_id.lower() == "exit":
                break
            else:
                chat = vk.messages.getChat(chat_id=chat_id)
                chat_title = chat["title"]
                chat_id = chat["id"]
                chat_users = chat["users"]
                
                user = vk.users.get(user_ids=chat_users)
                
                print('Title: ', chat_title)
                print('ID: ', chat_id)
                print('Количество участников: ', len(chat_users))
                enumeration(user, chat_users)
                            
    except vk_api.exceptions.ApiError as e:
        print(e)
        print(f'Диалога {chat_id} не существует!')
        group_chat_get_user_info()

if __name__ == '__main__':
    group_chat_get_user_info()

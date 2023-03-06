import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# Token file
from key import main_token

# authorization
vk_session = vk_api.VkApi(token=main_token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


# definition is it a person or a bot by ID
def user_detector(user_id):
    if user_id < 0:
        user_name = 'bot'
        print(user_name)
    else:
        user = vk.users.get(user_ids=user_id)
        user_name = user[0]['first_name'] + ' ' + user[0]['last_name'] + " " + str(user[0]['id'])
        print(user_name)


def main():
    print("Worked")
    print()

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:

            print('New Message:')

            if event.from_me:
                print('from me for: ')
                user_detector(event.user_id)
            elif event.to_me:
                print('For me from: ')
                user_detector(event.user_id)
            if event.from_user:
                print('From the user "event.from_user" ')
                print(user_detector(event.user_id))
            elif event.from_chat:
                user_detector(event.user_id)
                print(' in conversation ', event.chat_id)
            elif event.from_group:
                print('groups', event.group_id)
            print()
            print('Text: ', event.text)
            print()

            # the user types a message
        elif event.type == VkEventType.USER_TYPING:
            print('Typing... ')
            user_detector(event.user_id)
            if event.from_user:
                print(event.user_id)
                user_detector(event.user_id)
            elif event.from_group:
                print('Group Administrator', event.group_id)
        elif event.type == VkEventType.USER_TYPING_IN_CHAT:
            print('Typing ')
            user_detector(event.user_id)
            print('in conversation  ', event.chat_id)

        elif event.type == VkEventType.USER_ONLINE:
            print('User')
            user_detector(event.user_id)
            print('online', event.platform)
        elif event.type == VkEventType.USER_OFFLINE:
            print('User')
            user_detector(event.user_id)
            print('offline', event.offline_type)


if __name__ == '__main__':
    main()

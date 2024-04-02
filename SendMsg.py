# Для примера использования 2 методов
# def get_user_status(user_id):
#     status = session.method('status.get', {user_id: user_id})
#     print(status['text'])
#
#
# def set_user_status():
#     text = input()
#     vk.status.set(text=text)


import vk_api
from config import main_token, peer_id


def send_msg():
    while True:
        try:
            session = vk_api.VkApi(token=main_token)
            vk = session.get_api()
            msg = input("Введи сообщение: ")
            vk.messages.send(peer_id=peer_id, message=msg, random_id=0)
        except Exception as e:
            print(e)
            send_msg()


if __name__ == "__main__":
    send_msg()

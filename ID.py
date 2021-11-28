import vk_api
from mtok import token

vk_session = vk_api.VkApi(token=token)
vk_session.auth()
vk = vk_session.get_api()

def main():
	id = input("Введите ID: ")
	name = vk.user.get.(users.get = id)
	print(name['first_name','last_name'])
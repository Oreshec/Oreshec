import time
import vk_api
from config import main_token

def status_set():
    while True:
        session = vk_api.VkApi(token=main_token)
        vk = session.get_api()
        profile_info = vk.account.getProfileInfo()
        vk.status.set(text=time.asctime())
        status = session.method("status.get", {"user_id": profile_info['id']})
        print(status['text'])
        time.sleep(300)


if __name__ == '__main__':
    status_set()

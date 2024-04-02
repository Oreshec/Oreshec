import group_chat_get_user_info
import SendMsg
import VK_Reader_Message
import VK_Status_Set
import config
import asyncio


async def main():
    try:
        print('1. Status Set')
        print('2. Reader Message')
        choose = input()
        if choose == "1":
            await VK_Status_Set.status_set()
        elif choose == "2":
            await VK_Reader_Message.read()
        else:
            print("Не корректный ввод")
    except ExceptionGroup as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())

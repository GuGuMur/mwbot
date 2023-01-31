# from bot import Bot
# import asyncio
# async def main():
#     bot = Bot(
#             sitename="Guki",
#             api="",
#             index="",
#             username="GuBot",
#             password="MainBot@")
#     await bot.login()
#     r = await bot.get_section(page_name="用户:咕咕mur")
#     print(r)
#     await bot.close()

# if __name__ == "__main__":
#     asyncio.run(main())
from mwbot import arktool
arktool.gamedataPosition = "/home"
arktool.read_ark_cn_file("excel/item_table.json")
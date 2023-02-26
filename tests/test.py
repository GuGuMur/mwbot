from .bot import Bot
import nonebot
import asyncio
bot = Bot(
			sitename = "PRTS",
			api = "https://prts.wiki/api.php", 
			index = "https://prts.wiki/index.php",
			username="GuBot",
			password="MainBot@av89f6mgb7ns4m2ul8gaa8sdhq30altt")

if __name__ == "__main__":
    asyncio.run(main())
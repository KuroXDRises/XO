import asyncio
from bot import bot
import commands.start

if __name__=="__main__":
    asyncio.run(bot.polling())

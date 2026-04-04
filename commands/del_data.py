import os

from bot import bot
from bot import Dev

from db import *


@bot.message_handler(commands=["del_data"], func=lambda msg: msg.from_user.id in Dev)
async def delete_data(message):
    file_path = "users.json"

    if not os.path.exists(file_path):
        await bot.reply_to(
            message,
            "📁 File not found ❌"
        )
        return
  
    os.remove(file_path)
    await bot.reply_to(
        message,
        "📁 Deleted Successfully ✅"
    )

from bot import bot
from db import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

@bot.message_handler(commands=["profile", "me"])
async def profile_command(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if user == None:
        await bot.reply_to(
            message,
            "Register First"
        )
    text = f"""
    

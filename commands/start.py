from db import *
from bot import bot
from telebot.types import (
InlineKeyboardMarkup,
InlineKeyboardButton
)
pic = "https://i.ibb.co/Gv794MpQ/8aba2109900b.jpg"
@bot.message_handler(commands=["start"])
async def start_command(message):
    message.from_user.id
    user = get_user(user_id)

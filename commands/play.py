from bot import bot
from db import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

grid_data = {}

def make_5by5_grid():
    kb = InlineKeyboardMarkup(row_width=5)
    count = 1
    row = []
    for i in range(25):
        row.append(InlineKeyboardButton("⚪", callback_data=f"xo_{count}"))
        count += 1
        if len(row) == 5:
            kb.row(*row)
            row = []
    return kb

@bot.message_handler(commands=["play"])
async def play_xo(message):
    if message.chat.type != "private":
        await bot.reply_to(message, "Play only works in private")
        return

    buttons = make_5by5_grid()

    text = f"""
<b>[𝗫𝗢] 𝗠𝗔𝗧𝗖𝗛 𝗦𝗧𝗔𝗥𝗧𝗘𝗗 [𝗢𝗫]</b>

<b>Player 1:</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> ❌
<b>Player 2:</b> AI ⭕

<b>[xᴏ] 5×5 ɢʀɪᴅ ᴍᴀᴛᴄʜ sᴛᴀʀᴛᴇᴅ!</b>
"""

    await bot.send_message(message.chat.id, text, reply_markup=buttons, parse_mode="HTML")

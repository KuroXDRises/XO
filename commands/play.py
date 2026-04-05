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

    msg = await bot.send_message(message.chat.id, text, reply_markup=buttons, parse_mode="HTML")
    grid_data[message.from_user.id] = {"msg_id": msg.message_id, "grid": ["⚪"] * 25}
@bot.callback_query_handler(func=lambda call: call.data.startswith("xo_"))
async def buttons_handler(call):

    await bot.answer_callback_query(call.id)

    user = call.from_user.id
    if user not in grid_data:
        return await bot.answer_callback_query(call.id, "Start the game first by /play")

    slot = int(call.data.split("_")[1]) - 1

    if grid_data[user]["grid"][slot] != "⚪":
        return await bot.answer_callback_query(call.id, "Already selected")

    grid_data[user]["grid"][slot] = "❌"

    kb = InlineKeyboardMarkup(row_width=5)
    row = []

    for i in range(25):
        row.append(
            InlineKeyboardButton(
                grid_data[user]["grid"][i],
                callback_data=f"xo_{i+1}"
            )
        )
        if len(row) == 5:
            kb.row(*row)
            row = []

    await bot.edit_message_reply_markup(
        call.message.chat.id,
        grid_data[user]["msg_id"],
        reply_markup=kb
    )

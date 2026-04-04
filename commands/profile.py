from bot import bot
from db import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_rank(level):
    if level <= 20:
        return "Beginner"
    elif level <= 30:
        return "Novice"
    elif level <= 50:
        return "Intermediate"
    elif level <= 70:
        return "Advanced"
    elif level <= 90:
        return "Expert"
    else:
        return "Master"

@bot.message_handler(commands=["profile", "me"])
async def profile_command(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if user is None:
        return await bot.reply_to(message, "❌ Please register first!")

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Exit ❌", callback_data=f"exit_profile_{user_id}"))

    photos = await bot.get_user_profile_photos(user_id)
    text = f"""
<b>[𝗫𝗢] 𝗨𝗦𝗘𝗥 𝗣𝗥𝗢𝗙𝗜𝗟𝗘 [𝗫𝗢]</b>

<b>• User Info</b>
• Name: <a href="tg://user?id={user_id}">{user['name']}</a>
• Username: @{user['username']}
• Rank: {get_rank(user['level'])}

<b>• Stats</b>
• Wins: {user['wins']}
• Loses: {user['loses']}
• Total Matches: {user['total']}

<b>• Game Progress</b>
• Level: {user['level']}
• EXP: {user['exp']}/{user['max_exp']}
"""

    if photos.total_count == 0:
        await bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=kb)
        return

    photo = photos.photos[0][-1]
    await bot.send_photo(message.chat.id, photo.file_id, caption=text, parse_mode="HTML", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("exit_profile_"))
async def exit_profile(call):
    uid = call.data.split("_")[-1]
    if str(call.from_user.id) != uid:
        await bot.answer_callback_query(call.id, "❌ This button is not for you.", show_alert=True)
        return
    await bot.delete_message(call.message.chat.id, call.message.message_id)

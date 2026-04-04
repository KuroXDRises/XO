from bot import bot
from db import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_rank(level):
    if level <= 10:
        return "Beginner"
    elif level <= 20:
        return "Novice"
    elif level <= 30:
        return "Intermediate"
    elif level <= 40:
        return "Advanced"
    elif level <= 50:
        return "Expert"
    else:
        return "Master"

@bot.message_handler(commands=["profile", "me"])
async def profile_command(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if user is None:
        return await bot.reply_to(message, "❌ Please register first!")

    photos = await bot.get_user_profile_photos(user_id)
    if photos.total_count == 0:
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
        await bot.send_message(message.chat.id, text, parse_mode="HTML")
        return

    photo = photos.photos[0][-1]
    file_id = photo.file_id
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
    await bot.send_photo(message.chat.id, file_id, caption=text, parse_mode="HTML")

from db import *
from bot import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from Config import config
import os

# Your logs group ID (edit this)
LOGS_GROUP = config.LOGS_GRP

pic = "https://i.ibb.co/Gv794MpQ/8aba2109900b.jpg"


@bot.message_handler(commands=["start"])
async def start_command(message):
    user_id = message.from_user.id
    user = get_user(user_id)

    # Only private allowed
    if message.chat.type != "private":
        return await bot.reply_to(
            message,
            "⚠️ This command only works in private chats"
        )

    # IF NEW USER
    if user is None:

        data = {
            "name": message.from_user.first_name,
            "username": message.from_user.username,
            "level": 1,
            "exp": 0,
            "max_exp": 750,
            "total": 0,
            "wins": 0,
            "loses": 0
        }

        # Save DB
        save_user(user_id, data)

        # Log text for logs group
        log_text = f"""
🆕 **NEW USER REGISTERED**

**User Info:**  
• **Name:** {message.from_user.first_name}  
• **Username:** @{message.from_user.username if message.from_user.username else 'None'}  
• **User ID:** `{user_id}`  

**Game Stats Saved:**  
• Level: `{data['level']}`  
• EXP: `{data['exp']}/{data['max_exp']}`  
• Total Matches: `{data['total']}`  
• Wins: `{data['wins']}`  
• Loses: `{data['loses']}`  

🕒 Registered At: {message.date}
"""

        # Send log with quote
        await bot.send_message(
            LOGS_GROUP,
            log_text,
            reply_to_message_id=message.message_id
        )

        # User welcome message
        welcome_text = f"""
🎮 Welcome [{message.from_user.first_name}](tg://user?id={user_id}) to the Ultimate X-O Arena!

Choose your move wisely…  
Every grid matters in this 5x5 strategic battle.

✨ Features:
• Play 5x5 Advanced XO  
• Smart AI Opponent / Friend Match  
• Clean Grid Interface  
• Auto-Win Detection  
• Score Tracking System  

🚀 Ready to begin your match?
Good luck, Player — the board is yours. 🧠🔥
"""

        await bot.send_photo(
            message.chat.id,
            photo=pic,
            caption=welcome_text
        )
        return

    # IF OLD USER (already registered)
    text = """
👋 Welcome back, Player!

You're already registered and ready to play.

🎮 Continue your game anytime  
📊 Your stats are safely saved  
⚡ Tap any button to continue your journey!
"""

    await bot.send_photo(
        message.chat.id,
        photo=pic,
        caption=text
    )



# COMMAND: SEND DATABASE FILE
@bot.message_handler(commands=["dumpdb"])
async def send_database(message):
    file_path = "users.json"

    if not os.path.exists(file_path):
        await bot.send_message(message.chat.id, "❌ Database file not found!")
        return

    with open(file_path, "rb") as f:
        await bot.send_document(
            message.chat.id,
            f,
            caption="📦 Your database file (users.json)"
            )

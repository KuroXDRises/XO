from db import *
from bot import bot
from Config import config
import os

LOGS_GROUP = config.LOGS_GRP
pic = "https://i.ibb.co/Gv794MpQ/8aba2109900b.jpg"

@bot.message_handler(commands=["start"])
async def start_command(message):
    user_id = message.from_user.id
    user = get_user(user_id)

    if message.chat.type != "private":
        return await bot.reply_to(message, "⚠️ This command only works in private chats")

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

        save_user(user_id, data)

        log_text = (
            "🆕 *NEW USER REGISTERED*\n\n"
            "*User Info:*\n"
            f"• *Name:* {message.from_user.first_name}\n"
            f"• *Username:* @{message.from_user.username if message.from_user.username else 'None'}\n"
            f"• *User ID:* `{user_id}`\n\n"
            "*Game Stats Saved:*\n"
            f"• Level: `{data['level']}`\n"
            f"• EXP: `{data['exp']}/{data['max_exp']}`\n"
            f"• Total Matches: `{data['total']}`\n"
            f"• Wins: `{data['wins']}`\n"
            f"• Loses: `{data['loses']}`\n\n"
            f"🕒 Registered At: {message.date}"
        )

        await bot.send_message(LOGS_GROUP, log_text, parse_mode="Markdown")

        welcome_text = (
            f"🎮 Welcome [{message.from_user.first_name}](tg://user?id={user_id}) to the Ultimate X-O Arena!\n\n"
            "Choose your move wisely…\n"
            "Every grid matters in this 5x5 strategic battle.\n\n"
            "✨ *Features:*\n"
            "• Play 5x5 Advanced XO\n"
            "• Smart AI Opponent / Friend Match\n"
            "• Clean Grid Interface\n"
            "• Auto-Win Detection\n"
            "• Score Tracking System\n\n"
            "🚀 Ready to begin your match?\n"
            "Good luck, Player — the board is yours. 🧠🔥"
        )

        return await bot.send_photo(
            message.chat.id,
            photo=pic,
            caption=welcome_text,
            parse_mode="Markdown"
        )

    text = (
        "👋 *Welcome back, Player!*\n\n"
        "You're already registered and ready to play.\n\n"
        "🎮 Continue your game anytime\n"
        "📊 Your stats are safely saved\n"
        "⚡ Tap any button to continue your journey!"
    )

    await bot.send_photo(
        message.chat.id,
        photo=pic,
        caption=text,
        parse_mode="Markdown"
    )


@bot.message_handler(commands=["dumpdb"])
async def send_database(message):
    file_path = "users.json"

    if not os.path.exists(file_path):
        return await bot.send_message(message.chat.id, "❌ Database file not found!")

    with open(file_path, "rb") as f:
        await bot.send_document(
            message.chat.id,
            f,
            caption="📦 Your database file (users.json)"
            )

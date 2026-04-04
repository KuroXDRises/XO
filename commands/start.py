from db import *
from bot import bot
from Config import config
import os

LOGS_GROUP = config.LOGS_GRP
pic = "https://i.ibb.co/Gv794MpQ/8aba2109900b.jpg"

def escape_html(text):
    if not text:
        return ""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))

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
            "🆕 <b>NEW USER REGISTERED</b>\n\n"
            "<b>User Info:</b>\n"
            f"• <b>Name:</b> {escape_html(message.from_user.first_name)}\n"
            f"• <b>Username:</b> @{escape_html(message.from_user.username) if message.from_user.username else 'None'}\n"
            f"• <b>User ID:</b> <code>{user_id}</code>\n\n"
            "<b>Game Stats Saved:</b>\n"
            f"• Level: <code>{data['level']}</code>\n"
            f"• EXP: <code>{data['exp']}/{data['max_exp']}</code>\n"
            f"• Total Matches: <code>{data['total']}</code>\n"
            f"• Wins: <code>{data['wins']}</code>\n"
            f"• Loses: <code>{data['loses']}</code>\n\n"
            f"🕒 Registered At: {message.date}"
        )

        await bot.send_message(LOGS_GROUP, log_text, parse_mode="HTML")

        welcome_text = (
            f"🎮 Welcome <a href='tg://user?id={user_id}'>{escape_html(message.from_user.first_name)}</a> to the Ultimate X-O Arena!\n\n"
            "Choose your move wisely…\n"
            "Every grid matters in this 5x5 strategic battle.\n\n"
            "✨ <b>Features:</b>\n"
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
            parse_mode="HTML"
        )

    text = (
        "👋 <b>Welcome back, Player!</b>\n\n"
        "You're already registered and ready to play.\n\n"
        "🎮 Continue your game anytime\n"
        "📊 Your stats are safely saved\n"
        "⚡ Tap any button to continue your journey!"
    )

    await bot.send_photo(
        message.chat.id,
        photo=pic,
        caption=text,
        parse_mode="HTML"
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

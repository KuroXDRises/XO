from db import *
from bot import bot
from telebot.types import (
InlineKeyboardMarkup,
InlineKeyboardButton
)
from Config import config

pic = "https://i.ibb.co/Gv794MpQ/8aba2109900b.jpg"

@bot.message_handler(commands=["start"])
async def start_command(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if (user==None):
        text = f"""
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
Just choose a grid and let the battle start!

Good luck, Player — the board is yours. 🧠🔥
"""
        
        await bot.send_message(
            message.chat.id,
            pic,
            caption=text,
            reply_to_message_id=message.message_id
        )
        
    else:
        text = """
        👋 Welcome back, Player!

You're already registered and ready to play.

🎮 Continue your game anytime  
📊 Your stats are safely saved  
⚡ Tap any button to continue your journey!
"""
        await bot.send_message(
            message.chat.id,
            pic,
            caption=text,
            reply_to_message_id=message.message_id
        )



        

from bot import bot
from db import *

def get_lb_users():
    db = load_db()
    users = []
    for uid, data in db.items():
        users.append({
                  "uid": uid,
                  "name": data['name'],
                  "level": data['level'],
                  "exp": data['exp']
        })
    users = sorted(
        users,
        key=lambda x:
        (x['level'],
        x['exp']),
        reverse=True
    )
    return users
@bot.message_handler(commands=["leaderboard"])
async def leaderboard_handler(message):
    top10 = get_lb_users()[:10]
    text = f"[𝗫𝗢] 𝗧𝗢𝗣 𝗣𝗟𝗔𝗬𝗘𝗥𝗦 [𝗫𝗢]\n\n"
    rank = 1
    for top in top10:
        text+=f"<b><i>{rank}• {top['name']} | {top['level']} | {top['exp']}</i></b>\n"
        rank+=1
    await bot.reply_to(
        message,
        text
    )
        

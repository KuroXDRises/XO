from bot import bot
from db import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

grid_data = {}

EMPTY = "⚪"
PLAYER = "❌"
AI = "⭕"

def make_5by5_grid():
    kb = InlineKeyboardMarkup(row_width=5)
    row = []
    for i in range(25):
        row.append(InlineKeyboardButton(EMPTY, callback_data=f"xo_{i+1}"))
        if len(row) == 5:
            kb.row(*row)
            row = []
    return kb

def check_win(b, s):
    for r in range(0, 25, 5):
        if all(b[r+i] == s for i in range(5)): return True
    for c in range(5):
        if all(b[c+i*5] == s for i in range(5)): return True
    if all(b[i*6] == s for i in range(5)): return True
    if all(b[4+i*4] == s for i in range(5)): return True
    return False

def get_ai_move(board):
    import random

    if random.random() < 0.40:
        empty = [i for i in range(25) if board[i] == EMPTY]
        return random.choice(empty) if empty else None

    for i in range(25):
        if board[i] == EMPTY:
            c = board.copy()
            c[i] = AI
            if check_win(c, AI):
                return i

    for i in range(25):
        if board[i] == EMPTY:
            c = board.copy()
            c[i] = PLAYER
            if check_win(c, PLAYER):
                return i

    empty = [i for i in range(25) if board[i] == EMPTY]
    return random.choice(empty) if empty else None

def check_draw(b):
    return EMPTY not in b

@bot.message_handler(commands=["play"])
async def play_xo(message):
    if message.chat.type != "private":
        await bot.reply_to(message, "Play only works in private")
        return
    txt = f"""
<code>┌───[ 𝗫𝗢 𝗚𝗔𝗠𝗘 𝗦𝗧𝗔𝗥𝗧𝗘𝗗 ]───┐</code>
<code>│                               │
│ Player : {message.from_user.first_name} ❌           │
│ AI     : 🤖 Bot ⭕              │
│                                │</code>
<code>└───────────────────┘</code>
"""
    msg = await bot.send_message(
        message.chat.id,
        txt,
        reply_markup=make_5by5_grid(),
        parse_mode="HTML"
    )
    grid_data[message.from_user.id] = {"msg_id": msg.message_id, "grid": [EMPTY]*25}

@bot.callback_query_handler(func=lambda c: c.data.startswith("xo_"))
async def buttons_handler(call):
    await bot.answer_callback_query(call.id)
    u = call.from_user.id
    if u not in grid_data: return
    s = int(call.data.split("_")[1]) - 1
    b = grid_data[u]["grid"]
    if b[s] != EMPTY: return
    b[s] = PLAYER
    if check_win(b, PLAYER):
        await bot.edit_message_text("❌ YOU WIN!", call.message.chat.id, grid_data[u]["msg_id"])
        return
    if check_draw(b):
        await bot.edit_message_text("🤝 DRAW!", call.message.chat.id, grid_data[u]["msg_id"])
        return
    a = get_ai_move(b)
    if a is not None: b[a] = AI
    if check_win(b, AI):
        await bot.edit_message_text("⭕ AI WINS!", call.message.chat.id, grid_data[u]["msg_id"])
        return
    if check_draw(b):
        await bot.edit_message_text("🤝 DRAW!", call.message.chat.id, grid_data[u]["msg_id"])
        return
    kb = InlineKeyboardMarkup(row_width=5)
    r = []
    for i in range(25):
        r.append(InlineKeyboardButton(b[i], callback_data=f"xo_{i+1}"))
        if len(r) == 5:
            kb.row(*r)
            r = []
    await bot.edit_message_reply_markup(call.message.chat.id, grid_data[u]["msg_id"], reply_markup=kb)

from bot import bot
from db import *

def get_lb_users():
    db = load_db()
    users = []
    for uid, data in db.items():
        users.append(
                  "_id": uid,
                  "name": data['name'],
                  "level": data['level'],
                  "exp": data['exp']}
        )
    users = sorted(
        users,
        key=lambda x:
        (x['level'],
        x['exp']),
        reverse=True
    )

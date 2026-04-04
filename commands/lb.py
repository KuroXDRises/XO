from bot import bot
from db import *

def get_lb_users():
    db = load_db()
    users = []

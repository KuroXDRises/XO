import os
import json
path = "users.json"
def load_db():
    if not os.path.exists(path):
        with open(path, "w") as x:
            json.dump({}, x, indent=4)
        return {}
    with open(path, "r") as x:
        return json.load(x)
def save_db(db):
    with open(path, "w") as x:
        json.dump(db, x, indent=4)
def update_db(user_id, key, value):
    db = load_db()
    user_id = str(user_id)
    if user_id not in db:
        db[user_id] = {}
    db[user_id][key] = value
    save_db(db)
def get_user(user_id):
    db = load_db()
    user_id = str(user_id)
    if user_id not in db:
        return None
    user_data = db[user_id]
    return user_data
def delete_user(user_id):
    db = load_db()
    user_id = str(user_id)
    if user_id not in db:
        return None
    del db[user_id]

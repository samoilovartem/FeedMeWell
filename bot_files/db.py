from datetime import datetime
from random import choice

import certifi
from config import config
from emoji import emojize
from pymongo import MongoClient

client = MongoClient(config.mongo_db_config.uri, tlsCAFile=certifi.where())

db = client[config.mongo_db_config.db_name]


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({'user_id': effective_user.id})
    if not user:
        user = {
            'user_id': effective_user.id,
            'first_name': effective_user.first_name,
            'last_name': effective_user.last_name,
            'username': effective_user.username,
            'chat_id': chat_id,
            'emoji': emojize(choice(config.user_emoji), use_aliases=True),
        }
        db.users.insert_one(user)
    return user


def save_form(db, user_id, form_data):
    user = db.users.find_one({'user_id': user_id})
    form_data['created'] = datetime.now()
    if 'form' not in user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'form': [form_data]}},
        )
    else:
        db.users.update_one(
            {'_id': user['_id']},
            {'$push': {'form': form_data}},
        )

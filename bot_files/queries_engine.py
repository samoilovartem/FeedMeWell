from random import choice, sample

from config import config
from db import db, get_or_create_user
from queries_engine_utils import check_if_price, send_user_recommendations
from telegram import ReplyKeyboardRemove


def process_user_form(update):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    if user['form'][-1]['allow_location'] == 'yes':
        result = find_restaurants_with_location(user)
        check_recommendations_type(update, user, result)
    else:
        result = find_restaurants_with_city(user)
        check_recommendations_type(update, user, result)


def check_recommendations_type(update, user, result):
    if user['form'][-1]['recommendation_type'] == 'All recommendations':
        send_all_restaurants(update, result)
    else:
        send_random_restaurant(update, result)


def find_restaurants_with_location(user):
    query = {
        "location": {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": user['form'][-1]['user_coordinates'],
                },
                "$maxDistance": user['form'][-1]['distance_for_recommendations'] * 1000,
            }
        },
        "rating": {'$gte': user['form'][-1]['restaurant_rating']},
        'cuisine_list': {'$in': user['form'][-1]['cuisine_choice_list']},
    }
    if check_if_price(user):
        query['price_category'] = user['form'][-1]['price_category']
        result = db[config.mongo_db_config.db_collection_name].find(query)
    else:
        result = db[config.mongo_db_config.db_collection_name].find(query)
    return result


def find_restaurants_with_city(user):
    query = {
        "ranking_geo": {'$regex': user['form'][-1]['user_city']},
        "rating": {'$gte': user['form'][-1]['restaurant_rating']},
        'cuisine_list': {'$in': user['form'][-1]['cuisine_choice_list']},
    }
    if check_if_price(user):
        query["price_category"] = user['form'][-1]['price_category']
        result = db[config.mongo_db_config.db_collection_name].find(query)
    else:
        result = db[config.mongo_db_config.db_collection_name].find(query)
    return result


def send_all_restaurants(update, result):
    result = list(result)
    if result:
        result_length = len(result)
        limit = int(config.restaurant_output_limit)
        if result_length > limit:
            random_items = sample(result, limit)
            for item in random_items:
                send_user_recommendations(update, item)
        else:
            for item in result:
                send_user_recommendations(update, item)
    else:
        update.message.reply_text(
            'Unfortunately, I didn`t find any restaurants that match your criteria.\n'
            'Please try to start again and change some filters',
            reply_markup=ReplyKeyboardRemove(),
        )


def send_random_restaurant(update, result):
    result = list(result)
    if result:
        item = choice(result)
        send_user_recommendations(update, item)
    else:
        update.message.reply_text(
            'Unfortunately, I didn`t find any restaurants that match your criteria.\n'
            'Please try to start again and change some filters',
            reply_markup=ReplyKeyboardRemove(),
        )

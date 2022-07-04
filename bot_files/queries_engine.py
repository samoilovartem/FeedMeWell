from pymongo.errors import BulkWriteError
from random import choice, sample
from settings import MONGO_DB_COLLECTION, RESTAURANT_OUTPUT_LIMIT
from db import db, get_or_create_user
from telegram import ReplyKeyboardRemove
from queries_engine_utils import send_user_recommendations, check_if_price


def process_user_form(update):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    if user['form'][-1]['allow_location'] == 'yes':
        result = find_restaurants_with_location(user)
        if user['form'][-1]['recommendation_type'] == 'All recommendations':
            send_all_restaurants(update, result)
        else:
            send_random_restaurant(update, result)
    else:
        result = find_restaurants_with_city(user)
        if user['form'][-1]['recommendation_type'] == 'All recommendations':
            send_all_restaurants(update, result)
        else:
            send_random_restaurant(update, result)


def find_restaurants_with_location(user):
    query = {"location": {"$nearSphere": {"$geometry": {"type": "Point",
                                                        "coordinates": user['form'][-1]['user_coordinates']},
                                          "$maxDistance": user['form'][-1]['distance_for_recommendations'] * 1000}},
             "rating": {'$gte': user['form'][-1]['restaurant_rating']},
             'cuisine_list': {'$in': user['form'][-1]['cuisine_choice_list']},
             }
    if check_if_price(user):
        query["price_category"] = {'$eq': user['form'][-1]['price_category']}
        result = db[MONGO_DB_COLLECTION].find(query)
    else:
        result = db[MONGO_DB_COLLECTION].find(query)
    return result


def find_restaurants_with_city(user):
    query = {"ranking_geo": {'$regex': user['form'][-1]['user_city']},
             "rating": {'$gte': user['form'][-1]['restaurant_rating']},
             'cuisine_list': {'$in': user['form'][-1]['cuisine_choice_list']},
             }
    if check_if_price(user):
        query["price_category"] = {'$eq': user['form'][-1]['price_category']}
        result = db[MONGO_DB_COLLECTION].find(query)
    else:
        result = db[MONGO_DB_COLLECTION].find(query)
    return result


def send_all_restaurants(update, result):
    result = list(result)
    try:
        if result:
            result_length = len(result)
            limit = RESTAURANT_OUTPUT_LIMIT
            if result_length > limit:
                random_items = sample(result, limit)
                for item in random_items:
                    send_user_recommendations(update, item)
            else:
                for item in result:
                    send_user_recommendations(update, item)
        else:
            update.message.reply_text('Unfortunately, I didn`t find any restaurants that match your criteria.\n'
                                      'Please try to start again and change some filters',
                                      reply_markup=ReplyKeyboardRemove())
    except BulkWriteError as bwe:
        print(bwe.details)


def send_random_restaurant(update, result):
    result = list(result)
    try:
        if result:
            item = choice(result)
            send_user_recommendations(update, item)
        else:
            update.message.reply_text('Unfortunately, I didn`t find any restaurants that match your criteria.\n'
                                      'Please try to start again and change some filters',
                                      reply_markup=ReplyKeyboardRemove())
    except BulkWriteError as bwe:
        print(bwe.details)

from pymongo.errors import BulkWriteError
from random import choice, choices

from bot_magic_utils import get_restaurants_with_location, get_restaurants_with_location_no_price, \
    get_restaurants_with_city, get_restaurants_with_city_no_price, send_user_recommendations, \
    check_if_price


def do_magic_with_location(user, update):
    if check_if_price(user):
        get_all_restaurants(user, update, get_restaurants_with_location)
    else:
        get_all_restaurants(user, update, get_restaurants_with_location_no_price)


def do_magic_with_city(user, update):
    if check_if_price(user):
        get_all_restaurants(user, update, get_restaurants_with_city)
    else:
        get_all_restaurants(user, update, get_restaurants_with_city_no_price)


def do_magic_with_location_random(user, update):
    if check_if_price(user):
        get_random_restaurant(user, update, get_restaurants_with_location)
    else:
        get_random_restaurant(user, update, get_restaurants_with_location_no_price)


def do_magic_with_city_random(user, update):
    if check_if_price(user):
        get_random_restaurant(user, update, get_restaurants_with_city)
    else:
        get_random_restaurant(user, update, get_restaurants_with_city_no_price)


def get_all_restaurants(user, update, function):
    try:
        result = list(function(user))
        if result:
            result_length = len(result)
            limit = 15
            if result_length >= limit:
                items = choices(result, k=limit)
                for item in items:
                    send_user_recommendations(update, item)
            else:
                for item in result:
                    send_user_recommendations(update, item)
        else:
            update.message.reply_text('Unfortunately, I didn`t find any restaurants that match your criteria.\n'
                                      'Please try to start again and change some filters')
    except BulkWriteError as bwe:
        print(bwe.details)


def get_random_restaurant(user, update, function):
    try:
        result = list(function(user))
        if result:
            item = choice(result)
            send_user_recommendations(update, item)
        else:
            update.message.reply_text('Unfortunately, I didn`t find any restaurants that match your criteria.\n'
                                      'Please try to start again and change some filters')
    except BulkWriteError as bwe:
        print(bwe.details)

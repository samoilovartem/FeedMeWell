from db import db
from telegram import ParseMode


def send_user_recommendations(update, item):
    update.message.reply_text(f"<b>Name:</b> {item.get('name', None)}\n"
                              f"<b>Address:</b> {item.get('address', None)}\n"
                              f"<b>Description:</b> \n{item.get('description', None)}\n"
                              f"<b>Website:</b> \n{item.get('website', None)}\n"
                              f"<b>Full info and reviews:</b> \n{item.get('web_url', None)}\n",
                              parse_mode=ParseMode.HTML)


def get_restaurants_with_location(user):
    result = db.restaurants_manila.find(
        {"location": {"$nearSphere": {"$geometry": {"type": "Point",
                                                    "coordinates": user['form'][-1]['user_coordinates']},
                                      "$maxDistance": user['form'][-1]['distance_for_recommendations'] * 1000}},
         "rating": {'$gte': user['form'][-1]['restaurant_rating']},
         'cuisine_list': {'$in': user['form'][-1]['cuisine_choice_list']},
         "price_category": {'$eq': user['form'][-1]['price_category']},
         }
    )
    return result


def get_restaurants_with_city(user):
    result = db.restaurants_manila.find(
        {"ranking_geo": {'$regex': user['form'][-1]['user_city']},
         "rating": {'$gte': user['form'][-1]['restaurant_rating']},
         'cuisine_list': {'$in': user['form'][-1]['cuisine_choice_list']},
         "price_category": {'$eq': user['form'][-1]['price_category']},
         }
    )
    return result


def get_restaurants_with_location_no_price(user):
    result = db.restaurants_manila.find(
        {"location": {"$nearSphere": {"$geometry": {"type": "Point",
                                                    "coordinates": user['form'][-1]['user_coordinates']},
                                      "$maxDistance": user['form'][-1]['distance_for_recommendations'] * 1000}},
         "rating": {'$gte': user['form'][-1]['restaurant_rating']},
         'cuisine_list': {'$in': user['form'][-1]['cuisine_choice_list']},
         }
    )
    return result


def get_restaurants_with_city_no_price(user):
    result = db.restaurants_manila.find(
        {"ranking_geo": {'$regex': user['form'][-1]['user_city']},
         "rating": {'$gte': user['form'][-1]['restaurant_rating']},
         'cuisine_list': {'$in': user['form'][-1]['cuisine_choice_list']},
         }
    )
    return result


def check_if_price(user):
    if user['form'][-1]['price_category'] != 0:
        return True
    else:
        return False

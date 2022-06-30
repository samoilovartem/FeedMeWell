from db import db
import pprint
from pymongo.errors import BulkWriteError
from telegram import ParseMode


def do_magic_with_location(user, update):
    try:
        for doc in db.restaurants_manila.find(
                {"location": {"$nearSphere": {"$geometry": {"type": "Point",
                                                            "coordinates": user['form'][-1]['user_coordinates']},
                                              "$maxDistance": user['form'][-1]['distance_for_recommendations'] * 1000}},
                 "rating": {'$gte': user['form'][-1]['restaurant_rating']},
                 'cuisine_list': {'$in': user['form'][-1]['cuisine_choice_list']},
                 "price_category": {'$eq': user['form'][-1]['price_category']},
                 }
        ):
            pprint.pprint(doc['name'])
            if doc:
                send_user_recommendations(update, doc)
            else:
                update.message.reply_text('Unfortunately, I didn`t find any restaurants that match your criteria\n'
                                          'Please try to start again and change some filters')
    except BulkWriteError as bwe:
        print(bwe.details)


def do_magic_with_city(user, update):
    try:
        for doc in db.restaurants_manila.find(
                {"ranking_geo": {'$regex': user['form'][-1]['user_city']},
                 "rating": {'$gte': user['form'][-1]['restaurant_rating']},
                 'cuisine_list': {'$in': user['form'][-1]['cuisine_choice_list']},
                 "price_category": {'$eq': user['form'][-1]['price_category']},
                 }
        ):
            pprint.pprint(doc['name'])
            if doc:
                send_user_recommendations(update, doc)
            else:
                update.message.reply_text('Unfortunately, I didn`t find any restaurants that match your criteria\n'
                                          'Please try to start again and change some filters')
    except BulkWriteError as bwe:
        print(bwe.details)


def send_user_recommendations(update, doc):
    update.message.reply_text(f"<b>Name:</b> {doc.get('name', None)}\n"
                              f"<b>Address:</b> {doc.get('address', None)}\n"
                              f"<b>Description:</b> \n{doc.get('description', None)}\n"
                              f"<b>Website:</b> \n{doc.get('website', None)}\n"
                              f"<b>Full info and reviews:</b> \n{doc.get('web_url', None)}\n",
                              parse_mode=ParseMode.HTML)

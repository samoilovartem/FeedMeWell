from db import db
import pprint
from pymongo.errors import BulkWriteError
from random import choice


def find_restaurants():
    try:
        result = list(db.restaurants_manila.find(
                {"ranking_geo": {'$regex': "Taguig"},
                 "rating": {'$gte': 4.0},
                 'cuisine_list': {'$in': ['Spanish', 'Bar', 'Wine Bar']},
                 "price_category": {'$eq': 2},
                 }
        ))
        if result:
            print('There is a result')
            random_restaurant = choice(result)
            pprint.pprint(random_restaurant['name'])
        else:
            print('No results')
    except BulkWriteError as bwe:
        print(bwe.details)


def find_restaurants2():
    try:
        # db.restaurants_manila.create_index([("location", pymongo.GEOSPHERE)])
        for doc in db.restaurants_manila.find(
                {"location": {
                    "$nearSphere": {
                        "$geometry": {
                            "type": "Point",
                            "coordinates": [121.052249, 14.547731]
                        },
                        "$maxDistance": 3000}},
                    "rating": {'$gte': 4.5},
                    'cuisine_list': {'$in': ['Spanish', 'European', 'Bar']},
                    "price_category": {'$eq': 2}
                }
        ):
            pprint.pprint(type(doc))
            print('-' * 20)
    except BulkWriteError as bwe:
        print(bwe.details)


def find_bad_objects():
    for num, item in enumerate(db.restaurants_manila.find({'latitude': None})):
        print(num, item['_id'])


def delete_bad_objects():
    db.restaurants_manila.delete_many(
        {'latitude': None}
    )


if __name__ == '__main__':
    """This query creates a new field using existing fields` values as a reference"""
    # db.restaurants.update_many(
    #     {},
    #     [{'$set': {'approximate_price': '$price_level'}}])
    """This query creates a new field using existing fields` values as a reference + creating
    a new field inside that field"""
    # db.restaurants_manila.update_many(
    #     {},
    #     [{'$set': {'location': {'type': 'Point', 'coordinates': ['$longitude', '$latitude']}}}]
    # )
    """This query changes data type from a string to a float (Double). 
    Also can be used $toDecimal for decimal"""
    # db.restaurants_manila.update_many(
    #     {'rating': {'$exists': True, '$type': 'string'}},
    #     [{'$set': {'rating': {'$toDouble': '$rating'}}}]
    # )
    """This query deletes the specific fields inside a collection"""
    # db.restaurants_manila.update_many(
    #     {},
    #     {'$unset': {'parent_display_name': 1,
    #                 'gb_distance': 1,
    #                 'preferred_map_engine': 1,
    #                 'write_review': 1}},
    # )
    """This query creates a new field using existing fields` values inside a nested dict and list 
    as a reference"""
    # db.restaurants_manila.update_many(
    #     {},
    #     [{'$set': {'cuisine_list': '$cuisine.name'}}]
    # )
    # find_restaurants()
    # db.restaurants_manila.update_many(
    #     {'price_level': {'$exists': True, '$eq': '$$$$'}},
    #     [{'$set': {'price_category': 3}}]
    # )
    # for item in db.restaurants_manila.find({'ranking_geo': 'Manila'}):
    #     pprint.pprint(item['address'])
    #     print('-' * 50)
    # for num, item in enumerate(db.restaurants_manila.find({'price_range': {'$eq': [0, 550]}})):
    #     print(num, item['name'])
    #     print('-' * 50)

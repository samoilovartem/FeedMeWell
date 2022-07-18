import pymongo

from db import db
import pprint
from pymongo.errors import BulkWriteError
from random import sample
import settings

query_location = {"location": {"$nearSphere": {"$geometry": {
    "type": "Point",
    "coordinates": [121.052249, 14.547731]
},
    "$maxDistance": 2000}},
    "rating": {'$gte': 4.5},
    'cuisine_list': {'$in': ['Seafood', 'French', 'Spanish']},
}
query_city = {"ranking_geo": {'$regex': 'Taguig'},
              "rating": {'$gte': 4.5},
              'cuisine_list': {'$in': ['Cafe', 'Seafood', 'Sushi', 'Italian', 'European']},
              "price_category": 2,
              }


def find_restaurants():
    try:
        result = list(db[settings.MONGO_DB_COLLECTION].find(query_city))
        if result:
            result_length = len(result)
            print(result_length)
            limit = 10
            print('There is a result')
            if result_length > limit:
                random_items = sample(result, limit)
                for item in random_items:
                    pprint.pprint(item['name'])
            else:
                for item in result:
                    pprint.pprint(item['name'])
        else:
            print('No results')
    except BulkWriteError as bwe:
        print(bwe.details)


def find_restaurants2():
    try:
        # db.restaurants_manila.create_index([("location", pymongo.GEOSPHERE)])
        for doc in db.restaurants_manila.find({
            {'$match':
                {"location": {
                    "$nearSphere": {
                        "$geometry": {
                            "type": "Point",
                            "coordinates": [121.052249, 14.547731]
                        },
                        "$maxDistance": 2000}},
                    "rating": {'$gte': 4},
                    'cuisine_list': {'$in': ['Spanish', 'European', 'Bar']},
                    "price_category": {'$eq': 2},
                }},
            {'$sample': {'size': settings.RESTAURANT_OUTPUT_LIMIT}},
        }):
            pprint.pprint(doc['name'])
            print('-' * 20)
    except BulkWriteError as bwe:
        print(bwe.details)


def find_bad_objects_based_on_field_and_value(collection_name, field, value):
    for num, item in enumerate(db[collection_name].find({field: value})):
        print(num, item['name'])


def delete_bad_objects():
    db.restaurants_batangas.delete_many(
        {'latitude': None}
    )


def from_string_to_float(collection_name, field):
    db[collection_name].update_many(
        {field: {'$exists': True, '$type': 'string'}},
        [{'$set': {field: {'$toDouble': f'${field}'}}}]
    )


def delete_fields(collection_name):
    fields_to_delete = ['doubleclick_zone', 'preferred_map_engine', 'ranking_geo_id',
                        'ranking_denominator', 'ranking_category', 'distance', 'distance_string',
                        'bearing', 'is_closed', 'open_now_text', 'is_long_closed',
                        'parent_display_name', 'is_jfy_enabled', 'nearest_metro_station', 'hours',
                        'is_candidate_for_contact_info_suppression', 'gb_distance', 'establishment_types',
                        'awards', 'category', 'subcategory', 'write_review']
    query = {'$unset': {'parent_display_name': 1}}
    for field in fields_to_delete:
        query['$unset'][field] = 1
    db[collection_name].update_many(
        {},
        query,
    )


def create_location(collection_name):
    db[collection_name].update_many(
        {},
        [{'$set': {'location': {'type': 'Point', 'coordinates': ['$longitude', '$latitude']}}}]
    )


def create_geo_index(collection_name):
    db[collection_name].create_index([("location", pymongo.GEOSPHERE)])


def create_field_based_on_other_fields(collection_name, new_field, ref_field):
    db[collection_name].update_many(
        {},
        [{'$set': {new_field: f'${ref_field}.name'}}]
    )


def find_all_values_of_particular_field(collection_name, field):
    for num, item in enumerate(db[collection_name].distinct(field)):
        print(num, item)


def create_price_category_based_on_price_level(collection_name, price_symbols, price_category):
    db[collection_name].update_many(
        {'price_level': {'$exists': True, '$eq': price_symbols}},
        [{'$set': {'price_category': price_category}}]
    )


if __name__ == '__main__':
    """This query creates a new field using existing fields` values as a reference"""
    # db.restaurants.update_many(
    #     {},
    #     [{'$set': {'approximate_price': '$price_level'}}])
    """This query creates a new field using existing fields` values inside a nested dict and list 
    as a reference"""
    # db.restaurants_manila.update_many(
    #     {},
    #     [{'$set': {'cuisine_list': '$cuisine.name'}}]
    # )
    # find_restaurants()
    # for item in db.restaurants_batangas.find({'name': 'Casa Marikit'}):
    #     pprint.pprint(item['ranking_geo'])
    #     print('-' * 50)
    # for num, item in enumerate(db.restaurants_manila.find({'price_range': {'$eq': [0, 550]}})):
    #     print(num, item['name'])
    #     print('-' * 50)
    # from_string_to_float('restaurants_batangas', 'longitude')
    # delete_fields('restaurants_batangas')
    # find_bad_objects_based_on_field('restaurants_batangas', 'price_level')
    # create_location('restaurants_batangas')
    # create_geo_index('restaurants_batangas')
    # create_field_based_on_other_fields('restaurants_batangas', 'cuisine_list', 'cuisine')
    # find_all_values_of_particular_field('restaurants_batangas', 'price_level')
    # create_price_category_based_on_price_level('restaurants_batangas', '$$$$', 3)



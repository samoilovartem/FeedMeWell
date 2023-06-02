import os
from random import sample

import certifi
import pymongo
from dotenv import find_dotenv, load_dotenv
from loguru import logger
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

load_dotenv(find_dotenv())

client = MongoClient(os.environ.get('MONGO_URI'), tlsCAFile=certifi.where())
db = client[os.environ.get('MONGO_DB')]

query_location = {
    "location": {
        "$nearSphere": {
            "$geometry": {"type": "Point", "coordinates": [121.052249, 14.547731]},
            "$maxDistance": 2000,
        }
    },
    "rating": {'$gte': 4.5},
    'cuisine_list': {'$in': ['Seafood', 'French', 'Spanish']},
}
query_city = {
    "ranking_geo": {'$regex': 'Taguig'},
    "rating": {'$gte': 4.5},
    'cuisine_list': {'$in': ['Cafe', 'Seafood', 'Sushi', 'Italian', 'European']},
    "price_category": 2,
}


def find_restaurants():
    try:
        result = list(db[os.environ.get('MONGO_DB_COLLECTION')].find(query_city))
        if result:
            result_length = len(result)
            logger.info(result_length)
            limit = 10
            logger.info('There is a result')
            if result_length > limit:
                random_items = sample(result, limit)
                for item in random_items:
                    logger.info(item['name'])
            else:
                for item in result:
                    logger.info(item['name'])
        else:
            logger.info('No results')
    except BulkWriteError as bwe:
        logger.error(bwe.details)


def find_restaurants2():
    try:
        for doc in db.restaurants_manila.find(
            {
                {
                    '$match': {
                        "location": {
                            "$nearSphere": {
                                "$geometry": {
                                    "type": "Point",
                                    "coordinates": [121.052249, 14.547731],
                                },
                                "$maxDistance": 2000,
                            }
                        },
                        "rating": {'$gte': 4},
                        'cuisine_list': {'$in': ['Spanish', 'European', 'Bar']},
                        "price_category": {'$eq': 2},
                    }
                },
                {'$sample': {'size': os.environ.get('RESTAURANT_OUTPUT_LIMIT')}},
            }
        ):
            logger.info(doc.get('name'))
            logger.info('-' * 20)
    except BulkWriteError as bwe:
        logger.error(bwe.details)


def find_objects_based_on_field_and_value(collection_name, field, value):
    for num, item in enumerate(db[collection_name].find({field: value})):
        logger.info('{}, {}', num, item.get('name'))


def delete_documents_that_have_field_and_value(collection_name, field, value):
    db[collection_name].delete_many({field: value})


def from_string_to_float(collection_name, field):
    db[collection_name].update_many(
        {field: {'$exists': True, '$type': 'string'}},
        [{'$set': {field: {'$toDouble': f'${field}'}}}],
    )


def delete_fields(collection_name, list_of_fields):
    query = {'$unset': {'parent_display_name': 1}}
    for field in list_of_fields:
        query['$unset'][field] = 1
    db[collection_name].update_many({}, query)


def create_location(collection_name):
    db[collection_name].update_many(
        {},
        [
            {
                '$set': {
                    'location': {
                        'type': 'Point',
                        'coordinates': ['$longitude', '$latitude'],
                    }
                }
            }
        ],
    )


def create_geo_index(collection_name):
    db[collection_name].create_index([("location", pymongo.GEOSPHERE)])


def create_field_based_on_other_fields(
    collection_name, new_field, ref_field, nested_field
):
    db[collection_name].update_many(
        {}, [{'$set': {new_field: f'${ref_field}.{nested_field}'}}]
    )


def find_all_values_of_particular_field(collection_name, field):
    for num, item in enumerate(db[collection_name].distinct(field)):
        logger.info('{}, {}', num, item)


def create_price_category_based_on_price_level(
    collection_name, price_symbols, price_category
):
    db[collection_name].update_many(
        {'price_level': {'$exists': True, '$eq': price_symbols}},
        [{'$set': {'price_category': price_category}}],
    )


def process_raw_data_script(collection_name):
    delete_documents_that_have_field_and_value(collection_name, 'latitude', None)
    logger.info('"Bad" documents have been deleted or not found')
    delete_fields(collection_name, fields_to_delete)
    logger.info('Unnecessary fields have been successfully deleted')
    from_string_to_float(collection_name, 'latitude')
    from_string_to_float(collection_name, 'longitude')
    from_string_to_float(collection_name, 'rating')
    logger.info(
        'Values of "latitude", "longitude" and "rating" have been transformed into a float'
    )
    create_location(collection_name)
    logger.info('Field "Location" has been successfully created')
    create_geo_index(collection_name)
    logger.info('GEO indexes have been created')
    create_field_based_on_other_fields(
        collection_name, 'cuisine_list', 'cuisine', 'name'
    )
    logger.info('Field "cuisine_list" has been successfully created')
    create_price_category_based_on_price_level(collection_name, '$', 1)
    create_price_category_based_on_price_level(collection_name, '$$ - $$$', 2)
    create_price_category_based_on_price_level(collection_name, '$$$$', 3)
    logger.info('All 3 price categories have been successfully created')


fields_to_delete = [
    'doubleclick_zone',
    'preferred_map_engine',
    'ranking_geo_id',
    'ranking_denominator',
    'ranking_category',
    'distance',
    'distance_string',
    'bearing',
    'is_closed',
    'open_now_text',
    'is_long_closed',
    'parent_display_name',
    'is_jfy_enabled',
    'nearest_metro_station',
    'hours',
    'is_candidate_for_contact_info_suppression',
    'gb_distance',
    'establishment_types',
    'awards',
    'category',
    'subcategory',
    'write_review',
]

if __name__ == '__main__':
    process_raw_data_script('restaurants_spb')

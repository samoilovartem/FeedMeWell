import json
import os

import requests
from dotenv import find_dotenv, load_dotenv
from loguru import logger

load_dotenv(find_dotenv())


def fetch_data(page):
    querystring = {'locationId': '298085', 'page': str(page)}
    headers = {
        'X-RapidAPI-Key': os.environ.get('RAPID_API_KEY'),
        'X-RapidAPI-Host': os.environ.get('RAPID_API_HOST'),
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()['data']['data']
    else:
        logger.exception(
            'Failed to fetch data for page {}: {}', page, response.status_code
        )
        return []


url = 'https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/searchRestaurants'

all_records = []

for page in range(1, 4):
    logger.info('Fetching data for page {}...', page)
    data = fetch_data(page)
    all_records.extend(data)

with open('tripadvisor_data.json', 'w') as outfile:
    json.dump(all_records, outfile, indent=4)

logger.info('Saved {} records to tripadvisor_data.json', len(all_records))

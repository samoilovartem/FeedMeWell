import requests
import settings
from db import db

querystring = {"location_id": "1758900", "restaurant_tagcategory": "10591",
               "restaurant_tagcategory_standalone": "10591", "currency": "PHP",
               "lunit": "km", "limit": "30", "min_rating": "3", "open_now": "false",
               "offset": "0", "lang": "en_US"}

headers = {
    "X-RapidAPI-Key": settings.RAPID_API_KEY,
    "X-RapidAPI-Host": settings.RAPID_API_HOST,
}


def get_data(db, amount):
    offset = 0
    for _ in range(amount):
        try:
            response = requests.request("GET", settings.RAPID_API_URL, headers=headers, params=querystring)
            result = response.json()
            db.restaurants_manila.insert_many(result['data'])
            querystring["offset"] = str(offset + 30)
            offset += 30
        except requests.exceptions.JSONDecodeError:
            continue


if __name__ == '__main__':
    get_data(db, 107)



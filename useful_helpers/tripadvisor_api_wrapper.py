import os
from urllib.parse import urlencode

import requests
from dotenv import find_dotenv, load_dotenv
from loguru import logger
from requests import Response

load_dotenv(find_dotenv())


class TripAdvisorAPI:
    """A class for checking the connection to the TripAdvisor Content API and making requests.

    Attributes:
        api_key (str): The unique API key to access Tripadvisor content.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.main_url = 'https://api.content.tripadvisor.com/api/v1/location/'

    def check_tripadvisor_connection(self):
        """
        Check the connection with TripAdvisor
        """
        url = f'{self.main_url}search?language=en&key={self.api_key}&searchQuery=London'

        response = self.get_response(url)
        status_code = response.status_code

        if 400 <= status_code <= 499:
            logger.exception('Client error: {}', response.text)

        if 500 <= status_code <= 599:
            logger.exception('Server error: {}', response.text)

    @staticmethod
    def get_response(url: str) -> Response:
        """
        Getting a response from the API call
        """
        headers = {'accept': 'application/json'}
        response = requests.get(url, headers=headers)
        return response

    def location_nearby_search(
        self,
        lat_long: str,
        category: str | None = None,
        radius: int | None = None,
        radius_unit: str | None = None,
        language: str = 'en',
    ) -> Response:
        """
        The Nearby Location Search request returns up to 10 locations found near the given latitude/longitude.
        You can use category ("hotels", "attractions", "restaurants", "geos"), phone number, address to search
        with more accuracy.

        Args:
            lat_long (str): Latitude/Longitude pair - eg. "42.3455,-71.10767".
            category (str): Filters result set based on property type.
              Valid options are "hotels", "attractions", "restaurants", and "geos".
            radius (int): Length of the radius from the provided latitude/longitude pair to filter results.
            radius_unit (str): Unit for length of the radius.
              Valid options are "km", "mi", "m" (km=kilometers, mi=miles, m=meters.
            language (str): The language in which to return results from the list of our Supported Languages.

        Returns:
            response: Response object with response data as application/json
        """

        params = {
            'key': self.api_key,
            'latLong': lat_long,
            'language': language,
        }

        if category:
            params['category'] = category
        if radius:
            params['radius'] = radius
        if radius_unit:
            params['radiusUnit'] = radius_unit

        encoded_params = urlencode(params)
        url = f'{self.main_url}nearby_search?{encoded_params}'

        response = self.get_response(url)
        return response

    @staticmethod
    def parse_nearby_search_response(response: Response) -> list:
        """
        Parsing the response from the Nearby Location Search request.
        """
        response_json = response.json()
        data = response_json.get('data')

        if not data:
            logger.exception('No data in response: {}', response_json)

        return data


if __name__ == "__main__":
    tripadvisor_api = TripAdvisorAPI(api_key=os.environ.get('TRIPADVISOR_API_KEY'))
    tripadvisor_api.check_tripadvisor_connection()

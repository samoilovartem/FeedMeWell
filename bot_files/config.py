from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


class MongoDBSettings(BaseConfig):
    uri: str
    db_name: str
    db_collection_name: str

    class Config:
        env_prefix = 'mongo_'


class RapidAPIConfig(BaseConfig):
    api_url: str
    api_key: str
    api_host: str

    class Config:
        env_prefix = 'rapid_'


class BotConfig(BaseConfig):
    api_Key: str
    price_categories: dict = {
        1: 'Inexpensive (up to 550 PHP)',
        2: 'Moderately expensive - expensive (from 551 up to 3000 PHP)',
        3: 'Very Expensive (from 3001 up to 100000 PHP)',
        4: 'Include all price ranges',
    }
    cuisine: tuple = (
        'Steakhouse',
        'Grill',
        'Bar',
        'Wine Bar',
        'Cafe',
        'Pizza',
        'Seafood',
        'Sushi',
        'European',
        'Spanish',
        'French',
        'Italian',
        'American',
        'Mediterranean',
        'Middle Eastern',
        'International',
        'Asian',
        'Taiwanese',
        'Chinese',
        'Filipino',
        'Japanese',
        'Korean',
        'Thai',
        'Mexican',
        'Latin',
    )
    user_emoji: list = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']
    available_cities: list = [
        'Taguig',
        'Pasay',
        'Makati',
        'Manila',
        'Quezon City',
        'Mandaluyong',
        'Pasig',
        'Paranaque',
        'Las Pinas',
    ]

    class Config:
        env_prefix = 'bot_'


class Config(BaseConfig):
    mongo_db_config: MongoDBSettings = MongoDBSettings()
    bot_config: BotConfig = BotConfig()
    rapid_api_config: RapidAPIConfig = RapidAPIConfig()
    restaurant_output_limit: int = 20


config = Config()

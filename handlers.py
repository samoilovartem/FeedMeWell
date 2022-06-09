from utils import *


def start(update, context):
    username = update.effective_user.first_name
    update.message.reply_text(
        f'Hello {username}!\nAre you ready to share your location for better recommendations?',
        reply_markup=yes_no_keyboard())
    return 'user_reply'


def process_user_reply(update, context):
    user_reply = update.message.text.lower()
    if user_reply == 'yes':
        update.message.reply_text(
            f'Please send your location',
            reply_markup=location_keyboard()
        )
        return 'user_location'
    else:
        update.message.reply_text('Please type your city`s name then')
        return 'input_user_city'


def get_user_location(update, context):
    user_coordinates = update.message.location
    # Here we do something with user_coordinates
    update.message.reply_text('Please choose a distance to show recommendations (no further than that)',
                              reply_markup=distance_keyboard())
    return 'user_coordinates'


def find_user_city(update, context):
    user_city = update.message.text
    # Here we look for user`s city in our DB.
    return 'user_city'


def get_user_budget(update, context):
    # We need to save chosen distance here
    update.message.reply_text('Please set your maximum budget (local currency) on the keyboard or just send a number',
                              reply_markup=maximum_budget_keyboard())
    return 'user_budget'


def get_food_type(update, context):
    # We need to save set budget here
    update.message.reply_text('Please choose types of cuisine you like (multiple choice)\n'
                              'Once done, please use "submit" button on the keyboard',
                              reply_markup=food_type_keyboard())
    return 'user_food_type'


def add_to_food_list(update, context):
    # Here we add all user`s choices into a list and do something with it
    pass


def submit_food_choice(update, context):
    update.message.reply_text('Please choose a restaurant`s rating (no lower that that)',
                              reply_markup=rating_keyboard())
    return 'user_food_choice'


def get_user_recommendations(update, context):
    update.message.reply_text('Would you like to receive all recommendations that match your criteria'
                              ' or just one random restaurant?',
                              reply_markup=user_recommendations_keyboard())
    return 'user_recommendations'


def send_all_recommendations(update, context):
    pass


def send_random_one(update, context):
    pass

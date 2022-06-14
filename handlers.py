from utils import *
from db import db, get_or_create_user, save_form


def start(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(
        f'Hello, {user["first_name"]}! {user["emoji"]}\n'
        f'Are you ready to share your location for better recommendations?',
        reply_markup=yes_no_keyboard())
    return 'user_reply'


def get_user_location(update, context):
    user_reply = update.message.text.lower()
    context.user_data['form'] = {'allow_location': user_reply}
    if user_reply == 'yes':
        update.message.reply_text(
            f'Please send your location',
            reply_markup=location_keyboard()
        )
        return 'user_location'
    else:
        update.message.reply_text('Please type your city`s name then')
        return 'user_city'


def get_user_preferred_distance(update, context):
    # Not the best code in the world but for now it does the job
    user_coordinates = update.message.location
    context.user_data['form']['user_coordinates'] = []
    context.user_data["form"]['user_coordinates'].append(user_coordinates['latitude'])
    context.user_data["form"]['user_coordinates'].append(user_coordinates['longitude'])
    # Here we do something with user_coordinates
    update.message.reply_text('Please choose a distance to show recommendations (no further than that)',
                              reply_markup=distance_keyboard())
    return 'user_preferred_distance'


def get_user_budget(update, context):
    # Here we can receive 2 possible options:
    # 1. User`s chosen distance for recommendations
    # 2. User`s input city
    user_input = update.message.text
    if user_input[0].isdigit():
        context.user_data['form']['distance_for_recommendations'] = user_input[0]
        update.message.reply_text(
            'Please set your maximum budget (local currency) on the keyboard or just send a number',
            reply_markup=maximum_budget_keyboard())
        return 'user_budget'
    else:
        context.user_data['form']['user_city'] = user_input
        update.message.reply_text(
            'Please set your maximum budget (local currency) on the keyboard or just send a number',
            reply_markup=maximum_budget_keyboard())
        return 'user_budget'


def get_user_food_type(update, context):
    context.user_data["form"]['cuisine_choice_list'] = []
    context.user_data['form']['max_budget'] = update.message.text
    update.message.reply_text('Please choose types of cuisine you like (multiple choice)\n'
                              'Once done, please use "submit" button on the keyboard',
                              reply_markup=food_type_keyboard())
    return 'user_food_type'


def add_to_user_food_list(update, context):
    # Here we add all user`s choices into a list
    context.user_data["form"]['cuisine_choice_list'].append(update.message.text)


def get_user_rating_choice(update, context):
    update.message.reply_text('Please choose a restaurant`s rating (no lower that that)',
                              reply_markup=rating_keyboard())
    return 'user_food_choice'


def get_user_recommendations(update, context):
    context.user_data['form']['restaurant_rating'] = update.message.text
    update.message.reply_text('Would you like to receive all recommendations that match your criteria'
                              ' or just one random restaurant?',
                              reply_markup=user_recommendations_keyboard())
    return 'user_recommendations'


def send_all_recommendations(update, context):
    context.user_data['form']['recommendation_type'] = update.message.text
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_form(db, user['user_id'], context.user_data['form'])


def send_random_one(update, context):
    context.user_data['form']['recommendation_type'] = update.message.text
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_form(db, user['user_id'], context.user_data['form'])

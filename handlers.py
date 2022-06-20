from utils_keyboards import *
from utils_functions import check_yes_or_no, check_city_or_distance
from db import db, get_or_create_user, save_form
from telegram.ext import ConversationHandler


def start(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(
        f'Hello, {user.get("first_name")}! {user.get("emoji")}\n'
        f'Are you ready to share your location for better recommendations?\n'
        f'(Press "No" if you are using desktop)',
        reply_markup=yes_no_keyboard())
    return 'user_reply'


def get_user_location(update, context):
    user_reply = update.message.text.lower()
    context.user_data['form'] = {'allow_location': user_reply}
    return check_yes_or_no(update, context, user_reply)


def get_user_preferred_distance(update, context):
    user_coordinates = update.message.location
    if user_coordinates:
        context.user_data['form']['user_coordinates'] = []
        context.user_data.get("form", {}).get('user_coordinates').append(user_coordinates['latitude'])
        context.user_data.get("form", {}).get('user_coordinates').append(user_coordinates['longitude'])
    # Here we do something with user_coordinates
    update.message.reply_text('Please choose a distance to show recommendations (no further than that)',
                              reply_markup=distance_keyboard())
    return 'user_preferred_distance'


def get_user_budget(update, context):
    # Here we can receive 2 possible options:
    # 1. User`s chosen distance for recommendations
    # 2. User`s input city
    user_input = update.message.text
    return check_city_or_distance(update, context, user_input)


def get_user_budget_back(update, context):
    update.message.reply_text(
        'Please set your maximum budget (local currency) on the keyboard or just send a number',
        reply_markup=maximum_budget_keyboard())
    return 'user_budget'


def get_user_food_type(update, context):
    context.user_data["form"]['cuisine_choice_list'] = []
    user_input = update.message.text
    if user_input.isdigit():
        context.user_data['form']['max_budget'] = update.message.text
        update.message.reply_text('Please choose types of cuisine you like (multiple choice)\n'
                                  'Once done, please use "submit" button on the keyboard',
                                  reply_markup=food_type_keyboard())
        return 'user_food_type'
    else:
        update.message.reply_text('Please enter a number!')


def add_to_user_food_list(update, context):
    # Here we add all user`s choices into a list
    cuisine_list = {'Italian', 'Spanish', 'Japanese', 'German', 'Korean', 'Chinese',
                    'American', 'French', 'Mexican', 'Greek', 'Russian', 'Thai'}
    user_input = update.message.text
    if user_input not in cuisine_list:
        update.message.reply_text('Please use keyboard`s data only!')
    else:
        context.user_data.get("form", {}).get('cuisine_choice_list').append(update.message.text)


def get_user_rating_choice(update, context):
    # Before adding cuisine_choice_list into DB we will make sure that there are no duplicates
    # by using set and then list
    context.user_data["form"]['cuisine_choice_list'] = list(set(
        context.user_data["form"]['cuisine_choice_list']))
    update.message.reply_text('Please choose a restaurant`s rating (no lower that that)',
                              reply_markup=rating_keyboard())
    return 'user_food_choice'


def get_user_recommendations(update, context):
    user_input = update.message.text
    if user_input.replace('.', '', 1).isdigit():
        context.user_data['form']['restaurant_rating'] = update.message.text
        update.message.reply_text('Would you like to receive all recommendations that match your criteria'
                                  ' or just one random restaurant?',
                                  reply_markup=user_recommendations_keyboard())
        return 'user_recommendations'
    else:
        update.message.reply_text('Please use keyboard`s data only!')


def send_all_recommendations(update, context):
    context.user_data['form']['recommendation_type'] = update.message.text
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_form(db, user.get('user_id'), context.user_data.get('form'))
    return ConversationHandler.END


def send_random_one(update, context):
    context.user_data.get['form']['recommendation_type'] = update.message.text
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_form(db, user.get('user_id'), context.user_data.get('form'))
    return ConversationHandler.END


def unknown_input(update, context):
    update.message.reply_text('Unfortunately, I don`t understand you :(\n'
                              'Please try to follow the instructions')
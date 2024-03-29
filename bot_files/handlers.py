from config import config
from db import db, get_or_create_user, save_form
from queries_engine import process_user_form
from telegram.ext import ConversationHandler
from utils_functions import (
    check_city_or_distance,
    check_user_price_category,
    check_yes_or_no,
)
from utils_keyboards import (
    distance_keyboard,
    food_type_keyboard,
    price_category_keyboard,
    rating_keyboard,
    user_recommendations_keyboard,
    yes_no_keyboard,
)


def start(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(
        f'Hello, {user.get("first_name")}! {user.get("emoji")}\n'
        f'Are you ready to share your location for better recommendations?\n'
        f'(Press "Yes" ONLY if you are using mobile phone)',
        reply_markup=yes_no_keyboard(),
    )
    return 'user_reply'


def get_user_location(update, context):
    user_reply = update.message.text.lower()
    context.user_data['form'] = {'allow_location': user_reply}
    return check_yes_or_no(update, user_reply)


def get_user_preferred_distance(update, context):
    user_coordinates = update.message.location
    if user_coordinates:
        context.user_data['form']['user_coordinates'] = []
        context.user_data.get('form', {}).get('user_coordinates').append(
            user_coordinates['longitude']
        )
        context.user_data.get('form', {}).get('user_coordinates').append(
            user_coordinates['latitude']
        )
    update.message.reply_text(
        'Please choose a distance to show recommendations (no further than that)',
        reply_markup=distance_keyboard(),
    )
    return 'user_preferred_distance'


def get_user_price_category(update, context):
    user_input = update.message.text.lower().capitalize()
    return check_city_or_distance(update, context, user_input)


def get_user_price_category_back(update, context):
    update.message.reply_text(
        'Please choose a price category on the keyboard',
        reply_markup=price_category_keyboard(),
    )
    return 'user_price_category'


def get_user_food_type(update, context):
    user_input = update.message.text
    context.user_data['form']['cuisine_choice_list'] = []
    return check_user_price_category(update, context, user_input)


def get_user_food_type_back(update, context):
    context.user_data['form']['cuisine_choice_list'] = []
    update.message.reply_text(
        'Please choose types of cuisine you like (multiple choice)\n'
        'Once done, please use "submit" button on the keyboard',
        reply_markup=food_type_keyboard(),
    )
    return 'user_food_type'


def add_to_user_food_list(update, context):
    user_input = update.message.text
    if user_input not in config.bot_config.cuisine:
        update.message.reply_text('Please use keyboard`s data only!')
    else:
        context.user_data.get('form', {}).get('cuisine_choice_list').append(
            update.message.text
        )


def get_user_rating_choice(update, context):
    user_input = update.message.text
    if user_input == 'Submit' and not context.user_data.get('form', {}).get(
        'cuisine_choice_list'
    ):
        update.message.reply_text('You must choose something!')
        return 'user_food_type'
    context.user_data['form']['cuisine_choice_list'] = list(
        set(context.user_data['form']['cuisine_choice_list'])
    )
    update.message.reply_text(
        'Please choose a restaurant`s rating (no lower that that)',
        reply_markup=rating_keyboard(),
    )
    return 'user_restaurant_rating'


def get_user_recommendations(update, context):
    user_input = update.message.text
    if user_input.replace('.', '', 1).isdigit():
        context.user_data['form']['restaurant_rating'] = float(update.message.text)
        update.message.reply_text(
            'Would you like to receive all recommendations that match your criteria'
            ' or just one random restaurant?',
            reply_markup=user_recommendations_keyboard(),
        )
        return 'user_recommendations'

    update.message.reply_text('Please use keyboard`s data only!')


def send_all_recommendations(update, context):
    context.user_data['form']['recommendation_type'] = update.message.text
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_form(db, user.get('user_id'), context.user_data.get('form'))
    process_user_form(update)
    return ConversationHandler.END


def send_random_one(update, context):
    context.user_data['form']['recommendation_type'] = update.message.text
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_form(db, user.get('user_id'), context.user_data.get('form'))
    process_user_form(update)
    return ConversationHandler.END


def unknown_input(update, context):
    update.message.reply_text(
        'Unfortunately, I don`t understand you :(\n'
        'Please try to follow the instructions'
    )


def unknown_input_outside_of_script(update, context):
    update.message.reply_text('To begin using bot, please use /start command')

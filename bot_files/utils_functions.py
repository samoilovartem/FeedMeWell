from config import config
from utils_keyboards import (
    food_type_keyboard,
    location_keyboard,
    price_category_keyboard,
)


def check_yes_or_no(update, user_reply):
    if user_reply == 'yes':
        update.message.reply_text(
            'Please send your location', reply_markup=location_keyboard()
        )
        return 'user_location'
    elif user_reply == 'no':
        update.message.reply_text('Please type your city`s name then')
        return 'user_city'
    update.message.reply_text('Please answer "Yes" or "No" only')


def check_city_or_distance(update, context, user_input):
    if user_input[0].isdigit():
        context.user_data['form']['distance_for_recommendations'] = int(user_input[0])
        return send_price_category_keyboard(update)

    if user_input in config.bot_config.available_cities:
        context.user_data['form']['user_city'] = user_input
        return send_price_category_keyboard(update)

    update.message.reply_text(
        'Unfortunately, I don`t know that city\n'
        'Available cities are:\n'
        'Taguig, Pasay, Makati, Manila, Quezon City, '
        'Mandaluyong, Pasig, Paranaque, Las Pinas'
    )


def send_price_category_keyboard(update):
    update.message.reply_text(
        'Please choose a price category on the keyboard',
        reply_markup=price_category_keyboard(),
    )
    return 'user_price_category'


def check_user_price_category(update, context, user_input):
    if user_input not in config.bot_config.price_categories.values():
        update.message.reply_text('Please use keyboard`s data only!')

    if user_input == config.bot_config.price_categories.get(1):
        context.user_data['form']['price_category'] = 1
    elif user_input == config.bot_config.price_categories.get(2):
        context.user_data['form']['price_category'] = 2
    elif user_input == config.bot_config.price_categories.get(3):
        context.user_data['form']['price_category'] = 3
    else:
        context.user_data['form']['price_category'] = 0

    update.message.reply_text(
        'Please choose types of cuisine you like (multiple choice)\n'
        'Once done, please use "submit" button on the keyboard',
        reply_markup=food_type_keyboard(),
    )
    return 'user_food_type'

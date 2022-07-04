from utils_keyboards import *
from settings import AVAILABLE_CITIES, PRICE_CATEGORIES


def check_yes_or_no(update, user_reply):
    if user_reply == 'yes':
        update.message.reply_text(
            f'Please send your location',
            reply_markup=location_keyboard()
        )
        return 'user_location'
    elif user_reply == 'no':
        update.message.reply_text('Please type your city`s name then')
        return 'user_city'
    else:
        update.message.reply_text('Please answer "Yes" or "No" only')


def check_city_or_distance(update, context, user_input):
    available_cities = AVAILABLE_CITIES
    if user_input[0].isdigit():
        context.user_data['form']['distance_for_recommendations'] = int(user_input[0])
        update.message.reply_text(
            'Please set your maximum budget (local currency) on the keyboard or just send a number',
            reply_markup=maximum_budget_keyboard())
        return 'user_price_category'
    else:
        if user_input in available_cities:
            context.user_data['form']['user_city'] = user_input
            update.message.reply_text(
                'Please set your maximum budget (local currency) on the keyboard or just send a number',
                reply_markup=maximum_budget_keyboard())
            return 'user_price_category'
        else:
            update.message.reply_text(f'Unfortunately, I don`t know that city\n'
                                      'Known cities are:\n'
                                      'Taguig, Pasay, Makati, Manila, Quezon City, '
                                      'Mandaluyong, Pasig, Paranaque, Las Pinas')


def check_user_price_category(update, context, user_input):
    price_categories = PRICE_CATEGORIES
    if user_input in price_categories:
        if user_input == price_categories[0]:
            context.user_data['form']['price_category'] = 1
        elif user_input == price_categories[1]:
            context.user_data['form']['price_category'] = 2
        elif user_input == price_categories[2]:
            context.user_data['form']['price_category'] = 3
        else:
            context.user_data['form']['price_category'] = 0
        update.message.reply_text('Please choose types of cuisine you like (multiple choice)\n'
                                  'Once done, please use "submit" button on the keyboard',
                                  reply_markup=food_type_keyboard())
        return 'user_food_type'
    else:
        update.message.reply_text('Please use keyboard`s data only!')

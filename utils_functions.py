from utils_keyboards import *


def check_yes_or_no(update, context, user_reply):
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
    possible_cities = {'Taguig', 'Pasay', 'Makati',
                       'Manila', 'Quezon City', 'Mandaluyong',
                       'Pasig', 'Paranaque', 'Las Pinas'}
    if user_input[0].isdigit():
        context.user_data['form']['distance_for_recommendations'] = int(user_input[0])
        update.message.reply_text(
            'Please set your maximum budget (local currency) on the keyboard or just send a number',
            reply_markup=maximum_budget_keyboard())
        return 'user_price_category'
    else:
        if user_input in possible_cities:
            context.user_data['form']['user_city'] = user_input
            update.message.reply_text(
                'Please set your maximum budget (local currency) on the keyboard or just send a number',
                reply_markup=maximum_budget_keyboard())
            return 'user_price_category'
        else:
            update.message.reply_text('Unfortunately, I don`t know that city\n'
                                      'Known cities are:\n'
                                      'Taguig, Pasay, Makati, Manila, Quezon City, '
                                      'Mandaluyong, Pasig, Paranaque, Las Pinas')


def check_user_price_category(update, context, user_input):
    price_categories_list = {'Inexpensive (up to 550 PHP)',
                             'Moderately expensive - expensive (from 551 up to 3000 PHP)',
                             'Very Expensive (from 3001 up to 100000 PHP)'}
    if user_input in price_categories_list:
        if user_input == 'Inexpensive (up to 550 PHP)':
            context.user_data['form']['price_category'] = 1
        elif user_input == 'Moderately expensive - expensive (from 551 up to 3000 PHP)':
            context.user_data['form']['price_category'] = 2
        elif user_input == 'Very Expensive (from 3001 up to 100000 PHP)':
            context.user_data['form']['price_category'] = 3
        update.message.reply_text('Please choose types of cuisine you like (multiple choice)\n'
                                  'Once done, please use "submit" button on the keyboard',
                                  reply_markup=food_type_keyboard())
        return 'user_food_type'
    else:
        update.message.reply_text('Please use keyboard`s data only!')

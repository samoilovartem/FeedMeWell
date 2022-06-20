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

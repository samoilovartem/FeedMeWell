from telegram.ext import Updater, MessageHandler, Filters
import logging
import settings
from handlers import *

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.BOT_API_KEY, use_context=True)

    dp = mybot.dispatcher

    main_script = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(/start)$'), start)
        ],
        states={
            'user_reply': [MessageHandler(Filters.text, get_user_location)],
            'user_location': [MessageHandler(Filters.location, get_user_preferred_distance)],
            'user_city': [MessageHandler(Filters.text, get_user_price_category)],
            'user_preferred_distance': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(Filters.regex('^(0.2 km|0.5 km|1 km|2 km|3 km|4 km|5 km'
                                             '|6 km|7 km|8 km|9 km)$'),
                               get_user_price_category),
            ],
            'user_price_category': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(Filters.text, get_user_food_type),
            ],
            'user_food_type': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(Filters.regex('^(One step back)$'), get_user_price_category_back),
                MessageHandler(Filters.regex('^(Submit)$'), get_user_rating_choice),
                MessageHandler(Filters.text, add_to_user_food_list)
            ],
            'user_restaurant_rating': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(Filters.regex('^(One step back)$'), get_user_food_type_back),
                MessageHandler(Filters.text, get_user_recommendations)
            ],
            'user_recommendations': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(Filters.regex('^(One step back)$'), get_user_rating_choice),
                MessageHandler(Filters.regex('^(All recommendations)$'), send_all_recommendations),
                MessageHandler(Filters.regex('^(Random one)$'), send_random_one),
            ],
        },
        fallbacks=[
            MessageHandler(Filters.photo | Filters.sticker | Filters.video | Filters.document,
                           unknown_input)
        ],
    )

    dp.add_handler(main_script)
    dp.add_handler(MessageHandler(Filters.location, get_user_location))

    logging.info('The bot has started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()

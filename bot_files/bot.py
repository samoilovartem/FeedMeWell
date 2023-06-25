from config import config
from handlers import (
    ConversationHandler,
    add_to_user_food_list,
    get_user_food_type,
    get_user_food_type_back,
    get_user_location,
    get_user_preferred_distance,
    get_user_price_category,
    get_user_price_category_back,
    get_user_rating_choice,
    get_user_recommendations,
    send_all_recommendations,
    send_random_one,
    start,
    unknown_input,
    unknown_input_outside_of_script,
)
from loguru import logger
from telegram.ext import Filters, MessageHandler, Updater

logger.add('bot.log', format='{time} {level} {message}', level='INFO')


def main():
    mybot = Updater(token=config.bot_config.api_Key, use_context=True)

    dp = mybot.dispatcher

    main_script = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(/start)$'), start)],
        states={
            'user_reply': [MessageHandler(Filters.text, get_user_location)],
            'user_location': [
                MessageHandler(Filters.regex('^(/start)$'), start),
                MessageHandler(Filters.location, get_user_preferred_distance),
            ],
            'user_city': [
                MessageHandler(Filters.regex('^(/start)$'), start),
                MessageHandler(Filters.text, get_user_price_category),
            ],
            'user_preferred_distance': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(
                    Filters.regex(
                        '^(0.2 km|0.5 km|1 km|2 km|3 km|4 km|5 km'
                        '|6 km|7 km|8 km|9 km)$'
                    ),
                    get_user_price_category,
                ),
            ],
            'user_price_category': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(Filters.text, get_user_food_type),
            ],
            'user_food_type': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(
                    Filters.regex('^(One step back)$'), get_user_price_category_back
                ),
                MessageHandler(Filters.regex('^(Submit)$'), get_user_rating_choice),
                MessageHandler(Filters.text, add_to_user_food_list),
            ],
            'user_restaurant_rating': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(
                    Filters.regex('^(One step back)$'), get_user_food_type_back
                ),
                MessageHandler(Filters.text, get_user_recommendations),
            ],
            'user_recommendations': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(
                    Filters.regex('^(One step back)$'), get_user_rating_choice
                ),
                MessageHandler(
                    Filters.regex('^(All recommendations)$'), send_all_recommendations
                ),
                MessageHandler(Filters.regex('^(Random one)$'), send_random_one),
            ],
        },
        fallbacks=[
            MessageHandler(
                Filters.photo | Filters.sticker | Filters.video | Filters.document,
                unknown_input,
            )
        ],
    )

    dp.add_handler(main_script)
    dp.add_handler(
        MessageHandler(
            Filters.text
            | Filters.photo
            | Filters.sticker
            | Filters.video
            | Filters.document
            | Filters.location,
            unknown_input_outside_of_script,
        )
    )
    logger.info('The bot has started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()

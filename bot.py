from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging
import settings
from handlers import *

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.BOT_API_KEY, use_context=True)

    dp = mybot.dispatcher

    main_script = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(start)$'), start)
        ],
        states={
            'user_reply': [MessageHandler(Filters.text, process_user_reply)],
            'user_location': [MessageHandler(Filters.location, get_user_location)],
            'input_user_city': [MessageHandler(Filters.text, find_user_city)],
            'user_city': [MessageHandler(Filters.text, get_user_budget)],
            'user_coordinates': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(Filters.regex('^(0.5 km|1 km|2 km|3 km|4 km|5 km|Don`t use this option)$'),
                               get_user_budget),
            ],
            'user_budget': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(Filters.regex('^(One step back)$'), get_user_location),
                MessageHandler(Filters.text, get_food_type),
            ],
            'user_food_type': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(Filters.regex('^(One step back)$'), get_user_budget),
                MessageHandler(Filters.regex(
                    '^(Italian|Spanish|Japanese|German|Korean|Chinese|American|French|Mexican|Greek|'
                    'Russian|Thai|Don`t use this option)$'), add_to_food_list),
                MessageHandler(Filters.regex('^(Submit)$'), submit_food_choice),
            ],
            'user_food_choice': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(Filters.regex('^(One step back)$'), get_food_type),
                MessageHandler(Filters.regex(
                    '^(3.6|3.7|3.8|3.9|4.0|4.1|4.2|4.3|4.4|4.5|4.6|4.7|4.8|4.9|5.0'
                    '|Don`t use this option)$'), get_user_recommendations),
            ],
            'user_recommendations': [
                MessageHandler(Filters.regex('^(Start over)$'), start),
                MessageHandler(Filters.regex('^(One step back)$'), submit_food_choice),
                MessageHandler(Filters.regex('^(All recommendations)$'), send_all_recommendations),
                MessageHandler(Filters.regex('^(Random one)$'), send_random_one),
            ],
        },
        fallbacks=[

        ],
    )

    dp.add_handler(main_script)
    # dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.location, get_user_location))

    logging.info('The bot has started')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()

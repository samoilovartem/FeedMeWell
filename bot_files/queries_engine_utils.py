from telegram import ParseMode
from telegram import ReplyKeyboardRemove


def send_user_recommendations(update, item):
    update.message.reply_text(f"<b>Name:</b> {item.get('name', None)}\n"
                              f"<b>Address:</b> {item.get('address', None)}\n"
                              f"<b>Description:</b> \n{item.get('description', None)}\n"
                              f"<b>Website:</b> \n{item.get('website', None)}\n"
                              f"<b>Full info and reviews:</b> \n{item.get('web_url', None)}\n",
                              parse_mode=ParseMode.HTML,
                              reply_markup=ReplyKeyboardRemove())


def check_if_price(user):
    if user['form'][-1]['price_category'] != 0:
        return True
    else:
        return False




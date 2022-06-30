from telegram import ReplyKeyboardMarkup, KeyboardButton


def location_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton('Send my location', request_location=True)]],
                               one_time_keyboard=True)


def yes_no_keyboard():
    return ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True)


def distance_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['0.2 km', '0.5 km', '1 km', '2 km', '3 km', '4 km'],
            ['5 km', '6 km', '7 km', '8 km', '9 km'],
            ['Start over']
        ], one_time_keyboard=True
    )


def maximum_budget_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['Inexpensive (up to 550 PHP)'],
            ['Moderately expensive - expensive (from 551 up to 3000 PHP)'],
            ['Very Expensive (from 3001 up to 100000 PHP)'],
            ['Start over']
        ], one_time_keyboard=True
    )


def food_type_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['Steakhouse', 'Grill', 'Bar', 'Wine Bar'],
            ['Cafe', 'Pizza', 'Seafood', 'Sushi'],
            ['European', 'Spanish', 'French', 'Italian'],
            ['American', 'Mediterranean', 'Middle Eastern'],
            ['International', 'Asian', 'Taiwanese'],
            ['Chinese', 'Filipino', 'Japanese'],
            ['Korean', 'Thai', 'Mexican', 'Latin'],
            ['One step back', 'Start over'],
            ['Submit']
        ], one_time_keyboard=False
    )


def rating_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['3.0', '3.5', '4.0', '4.5', '5.0'],
            ['One step back', 'Start over'],
        ], one_time_keyboard=True
    )


def user_recommendations_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['All recommendations', 'Random one'],
            ['One step back', 'Start over'],
        ], one_time_keyboard=True
    )
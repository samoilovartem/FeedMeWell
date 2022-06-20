from telegram import ReplyKeyboardMarkup, KeyboardButton


def location_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton('Send my location', request_location=True)]],
                               one_time_keyboard=True)


def yes_no_keyboard():
    return ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True)


def distance_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['0.5 km', '1 km', '2 km', '3 km', '4 km', '5 km'],
            ['Start over']
        ], one_time_keyboard=True
    )


def maximum_budget_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['500', '1500', '2000', '2500', '3000'],
            ['Start over']
        ], one_time_keyboard=True
    )


def food_type_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['Italian', 'Spanish', 'Japanese', 'German'],
            ['Korean', 'Chinese', 'American', 'French'],
            ['Mexican', 'Greek', 'Russian', 'Thai'],
            ['One step back', 'Start over'],
            ['Submit']
        ], one_time_keyboard=False
    )


def rating_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['3.6', '3.7', '3.8', '3.9', '4.0'],
            ['4.1', '4.2', '4.3', '4.4', '4.5'],
            ['4.6', '4.7', '4.8', '4.9', '5.0'],
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
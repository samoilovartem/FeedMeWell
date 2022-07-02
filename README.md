# "FeedMeWell" Project

FeedMeWell is a bot for Telegram that will show a selection of restaurants/bars based on user`s criteria.

### Main features:

##### User-entered criteria (filters):

- _**Location**_ (no further than X km from user`s location or an option to choose available city)
- **_Price ranges_** (user can choose from 3 different price categories or include all restaurants)
- **_Restaurant`s rating_** (no lower than X)
- **_Type of cuisine_** (Multiple choice)
- **_Output type_** (option to get a random restaurant or all recommendations(limited to 10))

### Additional features (can be done):

1. Expanded criteria (type of music played at the restaurant, portion size)
2. Ability to reserve a table 
3. Adding web applications to bot (since Bot API 6.0)
4. Ability to add reviews with photos
5. Lifehacks and user`s advices (e.g.: book a table X, don't book a table Y, etc.)

### To be continued...

### Installation 

1. Clone the repository from GitHub
2. Create a virtual environment
3. Install requirements: `pip install requirements.txt`
4. Create a file `settings.py`
5. Fill it out:
```
BOT_API_KEY = 'Your telegram API key'
USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']

MONGO_URI = 'Your MongoDB URI'
MONGO_DB = 'Your MongoDB name'

RAPID_API_URL = "Your Rapid API url"
RAPID_API_KEY = "Your Rapid API key"
RAPID_API_HOST = "Your Rapid API host"

RESTAURANT_OUTPUT_LIMIT = 'Your output limit'
```
6. Go to "bot_files" directory
7. Start the bot: `python bot.py`





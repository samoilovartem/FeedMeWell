# "FeedMeWell" Project

FeedMeWell is a bot for Telegram that will show a selection of restaurants/bars based on user`s criteria.

### Main features:

##### User-entered criteria (filters):

- _**Location**_ (no further than X km from user`s location or an option to choose available city)
- **_Price ranges_** (user can choose from 3 different price categories or include all restaurants)
- **_Restaurant`s rating_** (no lower than X)
- **_Type of cuisine_** (Multiple choice)
- **_Output type_** (option to get a random restaurant or all recommendations(limited to 10))

### Installation

1. Clone the repository from GitHub
2. Install poetry (if not yet done)
3. Install requirements: `poetry install`
4. Create `.env` file
5. Fill it out:
```
BOT_API_KEY = 'Your telegram API key'

MONGO_URI = 'Your MongoDB URI'
MONGO_DB = 'Your MongoDB name'
MONGO_DB_COLLECTION = 'Your MongoDB collection name'

RAPID_API_URL = "Your Rapid API url"
RAPID_API_KEY = "Your Rapid API key"
RAPID_API_HOST = "Your Rapid API host"

RESTAURANT_OUTPUT_LIMIT = 'Your output limit'
```
6. Run `docker compose up`

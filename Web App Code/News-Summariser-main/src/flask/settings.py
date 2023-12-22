import dotenv
import os

dotenv.load_dotenv(override=True)

SEARCH_KEY = os.environ.get('bing_key')

# FOR GOOGLE CUSTOM SEARCH API #
# SEARCH_ID = os.environ.get('goo_id')
# SEARCH_KEY = os.environ.get('goo_key')

# FOR AWS DYNAMO DB #
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.environ.get('REGION_NAME')

SEARCH_URL = "https://bing-news-search1.p.rapidapi.com/news/search"

RESULT_COUNT=10

GMAIL_KEY=os.environ.get('gmail_key')
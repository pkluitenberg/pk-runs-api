import os
from dotenv import load_dotenv

load_dotenv()

STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_API_REFRESH_TOKEN = os.getenv('STRAVA_API_REFRESH_TOKEN')
STRAVA_ATHLETE_ID = os.getenv('STRAVA_ATHLETE_ID')
STRAVA_SUBSCRIPTION_VERIFICATION_TOKEN=os.getenv('STRAVA_SUBSCRIPTION_VERIFICATION_TOKEN')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
MONGOHOST = os.getenv('MONGOHOST')
MONGOPASSWORD = os.getenv('MONGOPASSWORD')
MONGOPORT = os.getenv('MONGOPORT')
MONGOUSER = os.getenv('MONGOUSER')
MONGO_URL = f'mongodb://{MONGOUSER}:{MONGOPASSWORD}@{MONGOHOST}:{MONGOPORT}'
MONGO_DB_NAME = 'pk-runs-db'
MONGO_ACTIVITIES_COLLECTION = 'activities'
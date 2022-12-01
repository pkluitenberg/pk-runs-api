import os

from dotenv import load_dotenv
from pymongo import MongoClient

from src.strava.strava_api import StravaApi
from src.models.event import Event

load_dotenv()

STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_API_REFRESH_TOKEN = os.getenv('STRAVA_API_REFRESH_TOKEN')
STRAVA_ATHLETE_ID = os.getenv('STRAVA_ATHLETE_ID')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
MONGOHOST = os.getenv('MONGOHOST')
MONGOPASSWORD = os.getenv('MONGOPASSWORD')
MONGOPORT = os.getenv('MONGOPORT')
MONGOUSER = os.getenv('MONGOUSER')


class StravaEvent:
    def validate(event: Event):
        # should have some validations on the events sent over
        pass

    def create(activity_id: str | int):
        strava_client = StravaApi(client_id=STRAVA_CLIENT_ID,
                                  client_secret=STRAVA_CLIENT_SECRET,
                                  refresh_token=STRAVA_API_REFRESH_TOKEN,
                                  athlete_id=STRAVA_ATHLETE_ID)
        activity_data = strava_client.get_activity_by_id(activity_id)

        mongo_client = MongoClient(
            f'mongodb://{MONGOUSER}:{MONGOPASSWORD}@{MONGOHOST}:{MONGOPORT}')
        db = mongo_client['pk-runs-db']
        collection = db['activities']

        if bool(collection.find_one({'id': activity_id})):
            print(f'Sorry! Activity {activity_id} already exists...')
        else:
            document_id = collection.insert_one(activity_data)
            print(f'Inserted activity {activity_id} Document ID: {document_id}')


    def delete(activity_id: str | int):
        mongo_client = MongoClient(
            f'mongodb://{MONGOUSER}:{MONGOPASSWORD}@{MONGOHOST}:{MONGOPORT}')
        db = mongo_client['pk-runs-db']
        collection = db['activities']

        activity_to_delte = {'id': activity_id}

        if bool(collection.find_one(activity_to_delte)):
            document_id = collection.delete_one(activity_to_delte)
            print(f'Deleted activity {activity_id} Document ID: {document_id}')
            
        else:
            print(f'Sorry! Activity {activity_id} doesn"t exist...')
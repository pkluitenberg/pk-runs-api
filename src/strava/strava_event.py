from pymongo import MongoClient

from src.constants import (MONGO_ACTIVITIES_COLLECTION, MONGO_DB_NAME,
                           MONGO_URL, STRAVA_API_REFRESH_TOKEN,
                           STRAVA_ATHLETE_ID, STRAVA_CLIENT_ID,
                           STRAVA_CLIENT_SECRET)
from src.models.event import Event
from src.strava.strava_api import StravaApi


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

        mongo_client = MongoClient(MONGO_URL)
        db = mongo_client[MONGO_DB_NAME]
        collection = db[MONGO_ACTIVITIES_COLLECTION]

        if bool(collection.find_one({'id': activity_id})):
            print(f'Sorry! Activity {activity_id} already exists...')
        else:
            document_id = collection.insert_one(activity_data).inserted_id
            print(
                f'Inserted activity {activity_id} Document ID: {document_id}')

    def delete(activity_id: str | int):
        mongo_client = MongoClient(MONGO_URL)
        db = mongo_client[MONGO_DB_NAME]
        collection = db[MONGO_ACTIVITIES_COLLECTION]

        activity_to_delete = {'id': activity_id}

        if bool(collection.find_one(activity_to_delete)):
            collection.delete_one(activity_to_delete)
            print(f'Deleted activity {activity_id}')

        else:
            print(f'Sorry! Activity {activity_id} doesn"t exist...')

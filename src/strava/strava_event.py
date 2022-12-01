from src.constants import (STRAVA_API_REFRESH_TOKEN, STRAVA_ATHLETE_ID,
                           STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET)
from src.database import Database
from src.models.event import Event
from src.strava.strava_api import StravaApi


class StravaEvent:
    def validate(event: Event):
        # should have some validations on the events sent over
        pass

    def create(activity_id: int):
        strava_client = StravaApi(client_id=STRAVA_CLIENT_ID,
                                  client_secret=STRAVA_CLIENT_SECRET,
                                  refresh_token=STRAVA_API_REFRESH_TOKEN,
                                  athlete_id=STRAVA_ATHLETE_ID)
        activity_data = strava_client.get_activity_by_id(activity_id)

        db = Database()
        db.insert_activity(activity_id=activity_data,
                           activity_data=activity_data)

    def delete(activity_id: int):
        db = Database()
        db.delete_activity(activity_id=activity_id)

    def update():
        pass

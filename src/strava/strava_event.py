from src.database import Database
from src.models.event import Event
from src.strava.strava_api import StravaApi


class StravaEvent:
    def validate(event: Event):
        # should have some validations on the events sent over
        pass

    def create(activity_id: int):
        strava_client = StravaApi()
        activity_data = strava_client.get_activity_by_id(activity_id)

        db = Database()
        db.insert_activity(activity_id=activity_data,
                           activity_data=activity_data)

    def delete(activity_id: int):
        db = Database()
        db.delete_activity(activity_id=activity_id)

    def update():
        pass

from src.database import Database
from src.models.event import Event
from src.strava.strava_api import StravaApi


class StravaEvent:
    @staticmethod
    def validate(event: Event):
        # should have some validations on the events sent over
        pass

    @staticmethod
    def create(activity_id: int):
        strava_client = StravaApi()
        activity_data = strava_client.get_activity_by_id(
            activity_id=activity_id)

        db = Database()
        db.insert_activity(activity_id=activity_id,
                           data=activity_data)

    @staticmethod
    def delete(activity_id: int):
        db = Database()
        return db.delete_activity(activity_id=activity_id)

    @staticmethod
    def update():
        pass

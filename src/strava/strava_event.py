import os

from dotenv import load_dotenv

from src.gcp.storage import (read_json_from_google_cloud_storage,
                             write_json_to_google_cloud_storage)
from src.strava.strava_api import StravaApi
from src.models.event import Event

load_dotenv()

STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_API_REFRESH_TOKEN = os.getenv('STRAVA_API_REFRESH_TOKEN')
STRAVA_ATHLETE_ID = os.getenv('STRAVA_ATHLETE_ID')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')


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
        stats = strava_client.get_athlete_stats(athlete_id=STRAVA_ATHLETE_ID)
        all_activities = read_json_from_google_cloud_storage(
            bucket=GCS_BUCKET_NAME, filename='allActivities.json')
        all_activities.append(activity_data)
        write_json_to_google_cloud_storage(
            all_activities, bucket=GCS_BUCKET_NAME, filename='allActivities.json')
        write_json_to_google_cloud_storage(
            stats, bucket=GCS_BUCKET_NAME, filename='allStats.json')

    def delete(activity_id: str | int):
        all_activities = read_json_from_google_cloud_storage(
            bucket=GCS_BUCKET_NAME, filename='allActivities.json')
        all_activities_filtered = [
            activity for activity in all_activities if activity.get('id') != activity_id]
        write_json_to_google_cloud_storage(
            all_activities_filtered, bucket=GCS_BUCKET_NAME, filename='allActivities.json')

        strava_client = StravaApi(client_id=STRAVA_CLIENT_ID,
                               client_secret=STRAVA_CLIENT_SECRET,
                               refresh_token=STRAVA_API_REFRESH_TOKEN,
                               athlete_id=STRAVA_ATHLETE_ID)

        stats = strava_client.get_athlete_stats(athlete_id=STRAVA_ATHLETE_ID)
        write_json_to_google_cloud_storage(
            stats, bucket=GCS_BUCKET_NAME, filename='allStats.json')

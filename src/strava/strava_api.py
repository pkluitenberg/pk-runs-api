import requests

from constants import (STRAVA_API_REFRESH_TOKEN, STRAVA_ATHLETE_ID,
                       STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET)


class StravaApi:
    url='https://www.strava.com/api/v3'

    def __init__(self):
        self.athlete_id = STRAVA_ATHLETE_ID
        self._client_id = STRAVA_CLIENT_ID
        self._client_secret = STRAVA_CLIENT_SECRET
        self._refresh_token = STRAVA_API_REFRESH_TOKEN
        self._access_token = self._refresh_access_token()
        

    def _refresh_access_token(self) -> str:
        refresh_token_url = f'https://www.strava.com/oauth/token?client_id={self.client_id}&client_secret={self.client_secret}&refresh_token={self.refresh_token}&grant_type=refresh_token'
        r = requests.post(refresh_token_url)
        return r.json().get('access_token')

    def _get(self, endpoint_url: str):
        r = requests.get(endpoint_url, headers={
            'Authorization': f'Bearer {self.access_token}'})
        r.raise_for_status()
        return r.json()

    def get_activities_by_page(self, per_page: int, page: int = 1):
        endpoint_url = f'{StravaApi.url}/athlete/activities?page={page}&per_page={per_page}'
        return self._get(endpoint_url)

    def get_athlete_stats(self):
        endpoint_url = f'{StravaApi.url}/athletes/{self.athlete_id}/stats'
        return self._get(endpoint_url)

    def get_activity_by_id(self, activity_id: int, include_all_efforts: bool = False):
        endpoint_url = f'{StravaApi.url}/activities/{activity_id}?include_all_efforts={include_all_efforts}'
        return self._get(endpoint_url)

    def get_all_activities(self, per_page: int = 100, page: int = 1):
        last_page = False
        all_activities = []
        while not last_page:
            activities = self.get_activities_by_page(
                per_page=per_page, page=page)
            if len(activities) < per_page:
                last_page = True
            all_activities.extend(activities)
            print(f'Retreiving activities... Page: {page} Activities: {len(activities)}')
            page = page+1
        return all_activities

    

from dataclasses import dataclass
from unittest.mock import Mock, patch, call

import pytest

from src.strava.strava_api import *

TEST_CLIENT_ID = 'test_client_id'
TEST_CLIENT_SECRET = 'test_client_secret'
TEST_REFRESH_TOKEN = 'test_refresh_token'
TEST_ATHLETE_ID = 12345
TEST_ACCESS_TOKEN = 'test_access_token'
TEST_RESPONSE = {'test': 'response'}


class TestStravaApi:
    @dataclass
    class Fixture:
        strava: StravaApi
        mock_refresh_access_token: Mock
        mock_get: Mock

    @pytest.fixture
    @patch('src.strava.strava_api.STRAVA_CLIENT_ID', TEST_CLIENT_ID)
    @patch('src.strava.strava_api.STRAVA_CLIENT_SECRET', TEST_CLIENT_SECRET)
    @patch('src.strava.strava_api.STRAVA_API_REFRESH_TOKEN', TEST_REFRESH_TOKEN)
    @patch('src.strava.strava_api.STRAVA_ATHLETE_ID', TEST_ATHLETE_ID)
    @patch('src.strava.strava_api.StravaApi._refresh_access_token', autospec=True)
    @patch('src.strava.strava_api.StravaApi._get', autospec=True)
    def setup(self, mock_get, mock_refresh_access_token):
        mock_refresh_access_token.return_value = TEST_ACCESS_TOKEN
        mock_get.return_value = TEST_RESPONSE

        strava = StravaApi()
        strava.get_activities_by_page(6, 9)
        strava.get_athlete_stats()
        strava.get_activity_by_id(45678, False)
        return TestStravaApi.Fixture(strava=strava,
                                     mock_refresh_access_token=mock_refresh_access_token,
                                     mock_get=mock_get)

    def test_class_attributes(self, setup: Fixture):
        assert setup.strava.url == 'https://www.strava.com/api/v3'
        assert setup.strava._client_id == TEST_CLIENT_ID
        assert setup.strava._client_secret == TEST_CLIENT_SECRET
        assert setup.strava._refresh_token == TEST_REFRESH_TOKEN
        assert setup.strava.athlete_id == TEST_ATHLETE_ID
        assert setup.strava._access_token == TEST_ACCESS_TOKEN

    def test_call_refresh_access_token(self, setup: Fixture):
        setup.mock_refresh_access_token.assert_called_once()

    def test_get_activities_by_page(self, setup: Fixture):
        setup.mock_get.assert_has_calls(calls=[call(
            setup.strava, 'https://www.strava.com/api/v3/athlete/activities?page=9&per_page=6')])

    def test_get_athlete_stats(self, setup: Fixture):
        setup.mock_get.assert_has_calls(calls=[call(
            setup.strava, f'https://www.strava.com/api/v3/athletes/{TEST_ATHLETE_ID}/stats')])

    def test_get_activity_by_id(self, setup: Fixture):
        setup.mock_get.assert_has_calls(calls=[call(
            setup.strava, 'https://www.strava.com/api/v3/activities/45678?include_all_efforts=False')])

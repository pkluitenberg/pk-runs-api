from unittest.mock import patch, Mock

import pytest

from src.strava.strava import *
from dataclasses import dataclass

TEST_CLIENT_ID = 'test_client_id'
TEST_CLIENT_SECRET = 'test_client_secret'
TEST_REFRESH_TOKEN = 'test_refresh_token'
TEST_ATHLETE_ID = 12345
TEST_ACCESS_TOKEN = 'test_access_token'


class TestConstructor:
    @dataclass
    class Fixture:
        strava: Strava
        mock_refresh_access_token: Mock

    @pytest.fixture
    @patch('src.strava.strava.Strava._refresh_access_token', autospec=True)
    def setup(self, mock_refresh_access_token):
        mock_refresh_access_token.return_value = TEST_ACCESS_TOKEN
        strava = Strava(client_id=TEST_CLIENT_ID,
                        client_secret=TEST_CLIENT_SECRET,
                        refresh_token=TEST_REFRESH_TOKEN,
                        athlete_id=TEST_ATHLETE_ID)
        return TestConstructor.Fixture(strava=strava,
                                       mock_refresh_access_token=mock_refresh_access_token)

    def test_class_attributes(self, setup: Fixture):
        assert setup.strava.client_id == TEST_CLIENT_ID
        assert setup.strava.client_secret == TEST_CLIENT_SECRET
        assert setup.strava.refresh_token == TEST_REFRESH_TOKEN
        assert setup.strava.athlete_id == TEST_ATHLETE_ID
        assert setup.strava.access_token == TEST_ACCESS_TOKEN

    def test_call_refresh_access_token(self, setup: Fixture):
        setup.mock_refresh_access_token.assert_called_once()


@patch('src.strava.strava.Strava._refresh_access_token', autospec=True)
@patch('src.strava.strava.Strava._get', autospec=True)
def test_get_activities_by_page(mock_get, mock_refresh_access_token):
    mock_refresh_access_token.return_value = TEST_ACCESS_TOKEN
    mock_get.return_value = 'test'
    strava = Strava(client_id=TEST_CLIENT_ID,
                    client_secret=TEST_CLIENT_SECRET,
                    refresh_token=TEST_REFRESH_TOKEN,
                    athlete_id=TEST_ATHLETE_ID)
    strava.get_activities_by_page(6, 9)
    mock_get.assert_called_once_with(strava,
                                     'https://www.strava.com/api/v3/athlete/activities?page=9&per_page=6')

@patch('src.strava.strava.Strava._refresh_access_token', autospec=True)
@patch('src.strava.strava.Strava._get', autospec=True)
def test_get_athlete_stats(mock_get, mock_refresh_access_token):
    mock_refresh_access_token.return_value = TEST_ACCESS_TOKEN
    mock_get.return_value = 'test'
    strava = Strava(client_id=TEST_CLIENT_ID,
                    client_secret=TEST_CLIENT_SECRET,
                    refresh_token=TEST_REFRESH_TOKEN,
                    athlete_id=TEST_ATHLETE_ID)
    strava.get_athlete_stats(12345)
    mock_get.assert_called_once_with(strava,
                                     'https://www.strava.com/api/v3/athletes/12345/stats')

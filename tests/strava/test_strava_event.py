from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

from src.strava.strava_event import StravaEvent


class TestStravaEvent:
    @dataclass
    class Fixture:
        mock_strava_api: Mock
        mock_database: Mock

    @pytest.fixture
    @patch('src.strava.strava_event.Database', autospec=True)
    @patch('src.strava.strava_event.StravaApi', autospec=True)
    def setup(self, mock_strava_api_constructor, mock_database_contructor):
        mock_strava_api = Mock()
        mock_strava_api_constructor.return_value = mock_strava_api
        mock_strava_api.get_activity_by_id.return_value = {'fake': 'activity'}

        mock_database = Mock()
        mock_database_contructor.return_value = mock_database
        mock_database.insert_activity.return_value = "inserted_id"
        mock_database.delete_activity.return_value = True

        StravaEvent.create(12345)
        StravaEvent.delete(12345)

        return TestStravaEvent.Fixture(
            mock_strava_api=mock_strava_api,
            mock_database=mock_database
        )

    def test_get_activity_by_id_called(self, setup: Fixture):
        setup.mock_strava_api.get_activity_by_id.assert_called_once_with(
            activity_id=12345)

    def test_insert_activity_called(self, setup: Fixture):
        setup.mock_database.insert_activity.assert_called_once_with(
            activity_id=12345, data={'fake': 'activity'})

    def test_delete_activity_called(self, setup: Fixture):
        setup.mock_database.delete_activity.assert_called_once_with(
            activity_id=12345
        )

from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app

TEST_GCS_BUCKET_NAME = 'pk-runs-data'


class TestRoot:
    @dataclass
    class Fixture:
        client: TestClient

    @pytest.fixture
    def setup(self):
        client = TestClient(app)
        return TestRoot.Fixture(client=client)

    def test_status_code_200(self, setup: Fixture):
        response = setup.client.get("/")
        assert response.status_code == 200

    def test_correct_response(self, setup: Fixture):
        response = setup.client.get("/")
        assert response.json() == 'wyd?'


class TestAllActivities:
    @dataclass
    class Fixture:
        response: Mock
        mock_database: Mock
        expected_fields_to_include: list

    @pytest.fixture(params=[{'input': '?fields=distance,time', 'expected_value': ['distance', 'time']},
                            {'input': '', 'expected_value': []}],
                    ids=['fields provided', 'no fields provided'])
    @patch('src.main.Database', autospec=True)
    def setup(self, mock_database_constructor, request):
        mock_database = Mock()
        mock_database_constructor.return_value = mock_database
        mock_database.find_all_activities.return_value = [
            {'id': "fake_activity_id"}]

        client = TestClient(app)
        response = client.get(f"/all_activities{request.param.get('input')}")
        return TestAllActivities.Fixture(response=response,
                                         mock_database=mock_database,
                                         expected_fields_to_include=request.param.get('expected_value'))

    def test_status_code_200(self, setup: Fixture):
        assert setup.response.status_code == 200

    def test_find_all_activities_called(self, setup: Fixture):
        setup.mock_database.find_all_activities.assert_called_once_with(
            fields_to_include=setup.expected_fields_to_include)

    def test_get_expected_return_value(self, setup: Fixture):
        assert setup.response.json() == [{'id': "fake_activity_id"}]


class TestAllStats:
    @dataclass
    class Fixture:
        response: Mock
        mock_strava_api: Mock

    @pytest.fixture
    @patch('src.main.StravaApi', autospec=True)
    def setup(self, mock_strava_api_constructor):
        mock_strava_api = Mock()
        mock_strava_api_constructor.return_value = mock_strava_api
        mock_strava_api.get_athlete_stats.return_value = {'stats': "are_fun"}

        client = TestClient(app)
        response = client.get("/stats")
        print(response)
        return TestAllStats.Fixture(response=response,
                                    mock_strava_api=mock_strava_api)

    def test_status_code_200(self, setup: Fixture):
        assert setup.response.status_code == 200

    def test_get_athlete_stats_called(self, setup: Fixture):
        setup.mock_strava_api.get_athlete_stats.assert_called_once_with()

    def test_get_expected_return_value(self, setup: Fixture):
        assert setup.response.json() == {'stats': "are_fun"}

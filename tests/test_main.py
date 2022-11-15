import pytest
from fastapi.testclient import TestClient

from src.main import app, GCS_BUCKET_NAME
from dataclasses import dataclass
from unittest.mock import patch, Mock


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
        mock_read_json_from_gcs: Mock

    @pytest.fixture
    @patch('src.main.read_json_from_google_cloud_storage', autospec=True)
    def setup(self, mock_read_json_from_gcs):
        mock_read_json_from_gcs.return_value = {'test': "response"}

        client = TestClient(app)
        response = client.get("/all_activities")
        print(response)
        return TestAllActivities.Fixture(response=response,
                                         mock_read_json_from_gcs=mock_read_json_from_gcs)

    def test_status_code_200(self, setup: Fixture):
        assert setup.response.status_code == 200

    def test_read_json_from_gcs_called(self, setup: Fixture):
        setup.mock_read_json_from_gcs.assert_called_once_with(
            bucket=GCS_BUCKET_NAME, filename='allActivities.json')

    def test_get_expected_return_value(self, setup: Fixture):
        assert setup.response.json() == {'test': "response"}


class TestAllStats:
    @dataclass
    class Fixture:
        response: Mock
        mock_read_json_from_gcs: Mock

    @pytest.fixture
    @patch('src.main.read_json_from_google_cloud_storage', autospec=True)
    def setup(self, mock_read_json_from_gcs):
        mock_read_json_from_gcs.return_value = {'test': "response"}

        client = TestClient(app)
        response = client.get("/all_stats")
        print(response)
        return TestAllStats.Fixture(response=response,
                                    mock_read_json_from_gcs=mock_read_json_from_gcs)

    def test_status_code_200(self, setup: Fixture):
        assert setup.response.status_code == 200

    def test_read_json_from_gcs_called(self, setup: Fixture):
        setup.mock_read_json_from_gcs.assert_called_once_with(
            bucket=GCS_BUCKET_NAME, filename='allStats.json')

    def test_get_expected_return_value(self, setup: Fixture):
        assert setup.response.json() == {'test': "response"}

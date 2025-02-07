import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .conftest import make_headers
from .example_loader import load_example


class TestSearchPostcode:
    endpoint = "search-postcode-or-place"

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_search_postcode(self, get_api_key):
        # Given
        expected_status_code = 200
        expected_body = load_example("search-postcode_v2.json")

        api_key = get_api_key["apikey"]
        search = "manchester"
        body = {}

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"api-version": "2", "apikey": api_key, "search": search},
            headers=make_headers(api_key),
            json=body
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_place_not_found(self, get_api_key):
        # Given
        expected_status_code = 500
        expected_body = load_example("search-postcode-invalid_v2.json")

        api_key = get_api_key["apikey"]
        search = "El Dorado".lower()
        body = {}

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"api-version": "2", "apikey": api_key, "search": search},
            headers=make_headers(api_key),
            json=body
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_invalid_api_version(self, get_api_key):
        # Given
        expected_status_code = 404
        expected_body = load_example("bad-api-version-resource-not-found.json")

        api_key = get_api_key["apikey"]
        bad_api_version = "1"
        body = {}

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"api-version": bad_api_version, "apikey": api_key},
            headers=make_headers(api_key),
            json=body
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

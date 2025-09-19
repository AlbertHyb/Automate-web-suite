import pytest
from http import HTTPStatus
import random
import string
import logging
import time

logger = logging.getLogger(__name__)

class AirportsPage:
    def __init__(self, api_client):
        self.api_client = api_client
        self.endpoint = "flights"  # No dejar la URL completa ni visible

    def create_airport(self, flights_data, headers):
        return self.api_client.make_request(
            method="POST",
            endpoint=self.endpoint,
            data=flights_data,
            headers=headers
        )


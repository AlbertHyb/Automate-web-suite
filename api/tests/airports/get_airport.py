import pytest
import logging

logging.basicConfig(
    filename='d:/Automate-web-suite/api/logs/error.log',  # Cambiado a error.log
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class AirportsPage:
    def __init__(self, api_client):
        self.api_client = api_client
        self.endpoint = "airports"  # No dejar la URL completa ni visible

    def create_airport(self, airport_data, headers):
        return self.api_client.make_request(
            method="GET",
            endpoint=self.endpoint,
            data=airport_data,
            headers=headers
        )

    def get_airport_by_code(self, iata_code, headers):
        # Realiza una petición GET al endpoint /airports/{iata_code}
        return self.api_client.make_request(
            method="GET",
            endpoint=f"{self.endpoint}/{iata_code}",
            headers=headers
        )


@pytest.mark.parametrize("iata_code, expected_status", [
    ("MEX", 200),  # Código IATA de la Ciudad de México
    ("JFK", 200),  # Código IATA de Nueva York
    ("XXX", 404),  # Código IATA no existente (debería fallar)
])
def test_get_airport(iata_code, expected_status, api_client):
    airport_page = AirportsPage(api_client)
    headers = {"Content-Type": "application/json"}
    response = airport_page.get_airport_by_code(iata_code, headers)
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        # Ejemplo: Verifica que el nombre del aeropuerto esté en la respuesta
        assert "name" in data

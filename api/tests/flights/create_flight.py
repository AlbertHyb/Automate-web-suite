import datetime
import pytest
import logging
import requests
import time
import json
import traceback
from api.tests.aircfrafts.create_aircraft import create_aircraft_request


logger = logging.getLogger(__name__)


class FlightsPage:
    def __init__(self, api_client):
        self.api_client = api_client
        self.endpoint = "flights"  # No dejar la URL completa ni visible

    def create_flight(self, flight_data, headers):
        return self.api_client.make_request(
            method="POST",
            endpoint=self.endpoint,
            data=flight_data,
            headers=headers
        )

def create_flight_request(flight_data, api_client, auth_headers=None):
    flights_page = FlightsPage(api_client)
    # Headers básicos con autenticación
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if auth_headers:
        headers.update(auth_headers)

    start_time = time.time()
    model = flight_data.get("model", "UNKNOWN")
    logger.debug(f"Enviando solicitud POST para crear vuelos con modelo={model}")

    try:
        response = flights_page.create_flight(flight_data, headers=headers)

        duration = time.time() - start_time

        # Registrar la respuesta en el log con información detallada
        if response.status_code == 201:
            logger.info(
                f"[FLIGHTS_POST_SUCCESS] Modelo={model} | Status={response.status_code} | "
                f"Duración={duration:.3f}s"
            )
        else:
            try:
                error_data = response.json()
                error_detail = error_data.get('detail', 'No detail provided')
                logger.error(
                    f"[FLIGHTS_POST_ERROR] Modelo={model} | Status={response.status_code} | "
                    f"Duración={duration:.3f}s | "
                    f"Error={error_detail} | "
                    f"Headers enviados={headers} | "
                    f"Datos enviados={json.dumps(flight_data, indent=2, ensure_ascii=False)} | "
                    f"Respuesta completa: {json.dumps(error_data, indent=2, ensure_ascii=False)}"
                )
            except Exception:
                logger.error(
                    f"[FLIGHTS_POST_ERROR] Modelo={model} | Status={response.status_code} | "
                    f"Duración={duration:.3f}s | "
                    f"Headers enviados={headers} | "
                    f"Datos enviados={json.dumps(flight_data, indent=2, ensure_ascii=False)} | Respuesta no JSON: {response.text}"
                )
        return response
    except Exception as e:
        duration = time.time() - start_time
        error_type = type(e).__name__
        logger.error(
            f"[FLIGHT_POST_EXCEPTION] Modelo={model} | Tipo={error_type} | "
            f"Duración={duration:.3f}s | "
            f"Headers enviados={headers} | "
            f"Datos enviados={json.dumps(flight_data, indent=2, ensure_ascii=False)} | "
            f"Mensaje de error: {str(e)} | Traza: {traceback.format_exc()}"
        )
        # Crear una respuesta fallida similar a requests para mantener consistencia
        fake_response = requests.Response()
        fake_response.status_code = 500
        fake_response._content = json.dumps({
            "detail": str(e),
            "error_type": error_type,
            "endpoint": "flights"
        }).encode('utf-8')
        return fake_response

def get_aircraft_id_for_flight(api_client, auth_headers):
    """Obtiene el id de un avión válido creado usando el script de aviones."""
    aircraft_data = {
        "tail_number": str(int(time.time())),
        "model": "Boeing",
        "capacity": 200
    }
    response = create_aircraft_request(aircraft_data, api_client, auth_headers)
    if response.status_code == 201:
        return response.json()["id"]
    else:
        logger.error(f"No se pudo crear el avión para la prueba de vuelo. Status: {response.status_code}, Respuesta: {response.text}")
        return None

@pytest.mark.parametrize(
    "test_id, priority, flight_data, expected_status, description",
    [
        # Casos críticos
        (
            "FLIGHT_C001",
            "Critical",
            {
                "origin": "MEX",
                "destination": "CUN",
                "departure_time": "2025-09-24T10:00:00",
                "arrival_time": "2025-09-24T12:00:00",
                "base_price": 1000.0,
                # aircraft_id se asigna dinámicamente
            },
            201,
            "Creación de vuelo con todos los campos válidos"
        ),
        (
            "FLIGHT_C002",
            "Critical",
            {
                "origin": "MEX",
                "destination": "CUN",
                "departure_time": "2025-09-24T10:00:00",
                "arrival_time": "2025-09-24T12:00:00",
                "base_price": -100.0,
                # aircraft_id se asigna dinámicamente
                "available_seats": 180
            },
            422,
            "Creación de vuelo con precio negativo"
        ),
        (
            "FLIGHT_C003",
            "Critical",
            {
                "origin": "MEX",
                "destination": "CUN",
                "departure_time": "2025-09-24T10:00:00",
                "arrival_time": "2025-09-24T12:00:00",
                "base_price": 1000.0,
                # aircraft_id se asigna dinámicamente
                "available_seats": -5
            },
            422,
            "Creación de vuelo con asientos negativos"
        ),
        # Casos de prioridad media
        (
            "FLIGHT_M001",
            "Medium",
            {
                "origin": "MEX",
                "destination": "CUN",
                "departure_time": "2025-09-24T10:00:00",
                "arrival_time": "2025-09-24T12:00:00",
                "base_price": 1000.0,
                # Falta aircraft_id
                "available_seats": 180
            },
            422,
            "Creación de vuelo sin aircraft_id"
        ),
        (
            "FLIGHT_M002",
            "Medium",
            {
                "origin": "MEX",
                "destination": "BJC",
                "departure_time": "2025-09-24T10:00:00",
                "arrival_time": "2025-09-24T12:00:00",
                "base_price": 1000.0,
                # aircraft_id se asigna dinámicamente
                # Falta available_seats
            },
            422,
            "Creación de vuelo sin available_seats"
        ),

    ]
)
def test_create_flight_parametrized(test_id, priority, flight_data, expected_status, description, api_client, auth_headers):
    logger.info(f"Ejecutando prueba {test_id}: {description} [Prioridad: {priority}]")
    # Si el caso requiere aircraft_id, lo creamos dinámicamente
    if "aircraft_id" in flight_data or expected_status == 201:
        aircraft_id = get_aircraft_id_for_flight(api_client, auth_headers)
        if aircraft_id:
            flight_data["aircraft_id"] = aircraft_id
        else:
            pytest.skip("No se pudo crear un avión válido para la prueba de vuelo.")
    start_time = time.time()
    response = create_flight_request(flight_data, api_client, auth_headers)
    duration = time.time() - start_time
    if response.status_code != expected_status:
        try:
            error_message = response.json().get("detail", "No hay detalle disponible")
        except Exception:
            error_message = response.text
        logger.error(
            f"[TEST_FAILED] {test_id} | "
            f"Status esperado: {expected_status}, recibido: {response.status_code} | "
            f"Duración: {duration:.3f}s | "
            f"Error: {error_message} | "
            f"Parámetros: {json.dumps(flight_data, indent=2, ensure_ascii=False)}"
        )
    assert response.status_code == expected_status, \
        f"Se esperaba status {expected_status}, pero se recibió {response.status_code}. Respuesta: {response.text}"
    if expected_status == 201:
        data = response.json()
        logger.info(
            f"[TEST_SUCCESS] {test_id} | "
            f"Status: {response.status_code} | "
            f"Duración: {duration:.3f}s | "
            f"Datos enviados: {json.dumps(flight_data, indent=2, ensure_ascii=False)}"
        )
        assert "id" in data, "La respuesta debe contener el campo 'id'"
        assert "origin" in data, "La respuesta debe contener el campo 'origin'"
        assert "destination" in data, "La respuesta debe contener el campo 'destination'"
        assert "aircraft_id" in data, "La respuesta debe contener el campo 'aircraft_id'"
    logger.info(f"Prueba {test_id} completada con éxito")

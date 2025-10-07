import pytest
import random
import string
import logging
import time
import json
from http import HTTPStatus

logger = logging.getLogger(__name__)


def generate_random_tail_number(length=8):
    """Genera un tail_number aleatorio único."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def create_aircraft_request(aircraft_data, api_client, auth_headers=None):
    """Helper para crear un aircraft mediante petición HTTP."""

    logger.info("Intentando crear aircraft con datos: %s",
                json.dumps(aircraft_data, ensure_ascii=False))

    # Preparar headers
    headers = {}
    if auth_headers:
        headers.update(auth_headers)

    # Ejecutar petición HTTP
    start_time = time.time()
    response = api_client.make_request(
        endpoint="aircrafts",
        method="POST",
        data=aircraft_data,  # Cambiar json= por data=
        headers=headers
    )
    duration = time.time() - start_time

    logger.info("Status Code: %d | Duración: %.3fs",
                response.status_code, duration)
    logger.debug("Response: %s",
                 response.text[:200] if response.text else "Sin contenido")

    return response


@pytest.mark.parametrize(
    "test_id, priority, aircraft_data_template, expected_status, description",
    [
        # Casos críticos
        (
            "AIRCRAFT_C001",
            "Critical",
            {

                "model": "Boeing",
                "capacity": 200
            },
            201,
            "Creación de avión con todos los campos válidos"
        ),
        (
            "AIRCRAFT_C002",
            "Critical",
            {

                "model": "Boeing",
                "capacity": "xxx"  # Se envían string's
            },
            422,
            "Creación de avión con capacidad inválida (string)"
        ),
        (
            "AIRCRAFT_C003",
            "Critical",
            {

                "model": "Boeing",
                "capacity": ""  # Capacidad vacía
            },
            422,
            "Creación de avión con capacidad vacía"
        ),
        # Caso de prioridad media
        (
            "AIRCRAFT_M001",
            "Medium",
            {

                "model": "Boeing",
                # Falta capacity
            },
            422,
            "Creación de avión sin campo capacity"
        ),
        # Caso de prioridad baja
        (
            "AIRCRAFT_L001",
            "Low",
            {
                "tail_number": "X" * 300,  # tail_number extremadamente largo
                "model": "Boeing",
                "capacity": 200
            },
            422,
            "Creación de avión con tail_number extremadamente largo"
        ),
    ]
)
def test_create_aircraft(test_id, priority, aircraft_data_template, expected_status, description, api_client, auth_headers):
    logger.info(
        "Ejecutando prueba %s: %s [Prioridad: %s]", test_id, description, priority)

    # Generar aircraft_data dinámicamente con tail_number único
    aircraft_data = aircraft_data_template.copy()

    # Solo generar tail_number si no está especificado en el template (para casos de prueba específicos)
    if "tail_number" not in aircraft_data:
        aircraft_data["tail_number"] = generate_random_tail_number()

    # Ejecutar la prueba usando el helper
    response = create_aircraft_request(aircraft_data, api_client, auth_headers)

    # Verificar resultado
    if response.status_code != expected_status:
        try:
            error_message = response.json().get("detail", "No hay detalle disponible")
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            error_message = response.text

        logger.error(
            "[TEST_FAILED] %s | Status esperado: %s, recibido: %s | Error: %s | Datos enviados: %s",
            test_id,
            expected_status,
            response.status_code,
            error_message,
            json.dumps(aircraft_data, indent=2, ensure_ascii=False)
        )

    assert response.status_code == expected_status, \
        f"Se esperaba status {expected_status}, pero se recibió {response.status_code}. Respuesta: {response.text}"

    # Para casos exitosos, validamos la respuesta
    if expected_status == HTTPStatus.CREATED:  # Instead of 201
        response_data = response.json()
        logger.info(
            "[TEST_SUCCESS] %s | Status: %s | Respuesta: %s",
            test_id,
            response.status_code,
            json.dumps(response_data, indent=2, ensure_ascii=False)
        )

        # Validaciones básicas de la respuesta
        assert "id" in response_data, "La respuesta debe contener un ID de avión"
        if "tail_number" in aircraft_data and "tail_number" in response_data:
            assert response_data["tail_number"] == aircraft_data["tail_number"], "El número de cola no coincide"
        if "model" in aircraft_data and "model" in response_data:
            assert response_data["model"] == aircraft_data["model"], "El modelo de avión no coincide"
        if "capacity" in aircraft_data and "capacity" in response_data:
            assert response_data["capacity"] == aircraft_data["capacity"], "La capacidad no coincide"

    logger.info("Prueba %s completada con éxito", test_id)

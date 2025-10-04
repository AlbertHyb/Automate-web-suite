import pytest
import random
import string
import logging
import time
import traceback
import json
import requests
from api.pages.aircraft_page import AircraftPage

logger = logging.getLogger(__name__)


def generate_random_tail_number():
    """Genera un tail_number aleatorio de 5-10 caracteres usando solo letras y números."""
    length = random.randint(5, 10)
    # Usar letras y números para generar un tail_number válido
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))


def create_aircraft_request(aircraft_data, api_client, auth_headers=None):
    """Helper para crear aviones usando el Page Object Model.
    Args:
        aircraft_data: Datos del avión (tail_number, model, capacity)
        api_client: Instancia de ApiHelper
        auth_headers: Headers de autenticación adicionales
    Returns:
        requests.Response: Respuesta de la API
    """
    aircraft_page = AircraftPage(api_client)

    # Preparar headers con autenticación
    headers = {}
    if auth_headers:
        headers.update(auth_headers)

    start_time = time.time()
    model = aircraft_data.get("model", "UNKNOWN")
    logger.debug(
        f"Enviando solicitud POST para crear avión con modelo={model}")

    try:
        response = aircraft_page.create_aircraft(
            aircraft_data, headers=headers)
        duration = time.time() - start_time

        # Logging según el resultado
        if response.status_code == 201:
            logger.info(
                f"[AIRCRAFT_POST_SUCCESS] Modelo={model} | Status={response.status_code} | "
                f"Duración={duration:.3f}s"
            )
        else:
            try:
                error_data = response.json()
                error_detail = error_data.get('detail', 'No detail provided')
                logger.error(
                    f"[AIRCRAFT_POST_ERROR] Modelo={model} | Status={response.status_code} | "
                    f"Duración={duration:.3f}s | "
                    f"Error={error_detail} | "
                    f"Headers enviados={headers} | "
                    f"Datos enviados={json.dumps(aircraft_data, indent=2, ensure_ascii=False)} | "
                    f"Respuesta completa: {json.dumps(error_data, indent=2, ensure_ascii=False)}"
                )
            except:
                logger.error(
                    f"[AIRCRAFT_POST_ERROR] Modelo={model} | Status={response.status_code} | "
                    f"Duración={duration:.3f}s | "
                    f"Headers enviados={headers} | "
                    f"Datos enviados={json.dumps(aircraft_data, indent=2, ensure_ascii=False)} | "
                    f"Respuesta no JSON: {response.text}"
                )
        return response

    except Exception as e:
        duration = time.time() - start_time
        error_type = type(e).__name__
        logger.error(
            f"[AIRCRAFT_POST_EXCEPTION] Modelo={model} | Tipo={error_type} | "
            f"Duración={duration:.3f}s | "
            f"Headers enviados={headers} | "
            f"Datos enviados={json.dumps(aircraft_data, indent=2, ensure_ascii=False)} | "
            f"Mensaje de error: {str(e)} | "
            f"Traza: {traceback.format_exc()}"
        )


# --- Tests parametrizados ---

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
    """Prueba parametrizada para POST /aircrafts usando POM."""
    logger.info(
        f"Ejecutando prueba {test_id}: {description} [Prioridad: {priority}]")

    # Generar aircraft_data dinámicamente con tail_number único
    aircraft_data = aircraft_data_template.copy()

    # Solo generar tail_number si no está especificado en el template (para casos de prueba específicos)
    if "tail_number" not in aircraft_data:
        aircraft_data["tail_number"] = generate_random_tail_number()

    # Ejecutar la prueba usando el helper
    start_time = time.time()
    response = create_aircraft_request(aircraft_data, api_client, auth_headers)
    duration = time.time() - start_time

    # Verificar resultado
    if response.status_code != expected_status:
        try:
            error_message = response.json().get("detail", "No hay detalle disponible")
        except:
            error_message = response.text

        logger.error(
            f"[TEST_FAILED] {test_id} | "
            f"Status esperado: {expected_status}, recibido: {response.status_code} | "
            f"Duración: {duration:.3f}s | "
            f"Error: {error_message} | "
            f"Datos enviados: {json.dumps(aircraft_data, indent=2, ensure_ascii=False)}"
        )

    assert response.status_code == expected_status, \
        f"Se esperaba status {expected_status}, pero se recibió {response.status_code}. Respuesta: {response.text}"

    # Para casos exitosos, validamos la respuesta
    if expected_status == 201:
        response_data = response.json()
        logger.info(
            f"[TEST_SUCCESS] {test_id} | "
            f"Status: {response.status_code} | "
            f"Duración: {duration:.3f}s | "
            f"Respuesta: {json.dumps(response_data, indent=2, ensure_ascii=False)}"
        )

        # Validaciones básicas de la respuesta
        assert "id" in response_data, "La respuesta debe contener un ID de avión"
        if "tail_number" in aircraft_data and "tail_number" in response_data:
            assert response_data["tail_number"] == aircraft_data["tail_number"], "El número de cola no coincide"
        if "model" in aircraft_data and "model" in response_data:
            assert response_data["model"] == aircraft_data["model"], "El modelo de avión no coincide"
        if "capacity" in aircraft_data and "capacity" in response_data:
            assert response_data["capacity"] == aircraft_data["capacity"], "La capacidad no coincide"

    logger.info(f"Prueba {test_id} completada con éxito")

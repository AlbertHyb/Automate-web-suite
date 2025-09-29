import pytest
import random
import string
import logging
import time
import traceback
import json
import requests


logger = logging.getLogger(__name__)

class AircraftPage:
    def __init__(self, api_client):
        self.api_client = api_client
        self.endpoint = "aircrafts"  # No dejar la URL completa ni visible

    def create_aircraft(self, aircraft_data, headers):
        return self.api_client.make_request(
            method="POST",
            endpoint=self.endpoint,
            data=aircraft_data,
            headers=headers
        )

    def list_aircrafts(self, headers):
        return self.api_client.make_request(
            method="GET",
            endpoint=self.endpoint,
            headers=headers
        )


def create_aircraft_request(aircraft_data, api_client, auth_headers=None):
    aircraft_page = AircraftPage(api_client)
    # Headers básicos con autenticación
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if auth_headers:
        headers.update(auth_headers)

    start_time = time.time()
    model = aircraft_data.get("model", "UNKNOWN")
    logger.debug(f"Enviando solicitud POST para crear avión con modelo={model}")

    try:
        response = aircraft_page.create_aircraft(aircraft_data, headers=headers)

        duration = time.time() - start_time

        # Registrar la respuesta en el log con información detallada
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
        # Crear una respuesta fallida similar a requests para mantener consistencia
        fake_response = requests.Response()
        fake_response.status_code = 500
        fake_response._content = json.dumps({
            "detail": str(e),
            "error_type": error_type,
            "endpoint": "aircrafts"
        }).encode('utf-8')
        return fake_response


def generate_random_model():
    # Crear un código aleatorio que respete el límite de 10 caracteres
    # Formato: XX-NNNNN (donde X=letra, N=número)
    prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
    suffix = ''.join(random.choices(string.digits, k=5))
    return f"{prefix}-{suffix}"[:10]  # Asegurar que no exceda 10 caracteres


@pytest.mark.parametrize(
    "test_id, priority, aircraft_data, expected_status, description",
    [
        # Casos críticos
        (
            "AIRCRAFT_C001",
            "Critical",
            {
                "tail_number": generate_random_model(),
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
                "tail_number": generate_random_model(),
                "model": "Boeing",
                "capacity": "xxx" #Se envian string´s
            },
            422,
            "Creación de avión con capacidad negativa"
        ),
        (
            "AIRCRAFT_C003",
            "Critical",
            {
                "tail_number": generate_random_model(),
                "model": "Boeing",
                "capacity": "" #Capacidad vacía
            },
            422,
            "Creación de avión con rango negativo"
        ),
        # Caso de prioridad media
        (
            "AIRCRAFT_M001",
            "Medium",
            {
                "tail_number": generate_random_model(),
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
                "tail_number": "X" * 300,  # Modelo extremadamente largo
                "model": "Boeing",
                "capacity": 200
            },
            422,
            "Creación de avión con modelo extremadamente largo"
        ),
    ]
)
def test_create_aircraft(test_id, priority, aircraft_data, expected_status, description, api_client, auth_headers):
    logger.info(f"Ejecutando prueba {test_id}: {description} [Prioridad: {priority}]")

    # Ejecutar la prueba
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

    assert response.status_code == expected_status,  \
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


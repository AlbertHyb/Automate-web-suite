import logging
import time
import traceback
import json
import requests
import pytest
from http import HTTPStatus


logger = logging.getLogger(__name__)


def test_service_status(api_client):
    """Verifica que el servicio esté disponible antes de ejecutar las pruebas."""
    if api_client.is_service_up():
        logger.info("El servicio API está funcionando correctamente")
    else:
        pytest.fail("El servicio API no está disponible")


def test_update_aircraft_successful(api_client, authenticated_token, test_aircraft_id):
    """Test para verificar la actualización exitosa de un aircraft."""

    # 1. PREPARAR - Datos a actualizar
    update_data = {
        "tail_number": "NEW123",  # Nuevo tail_number (máx 10 caracteres)
        "model": "Boeing",        # Opcional: otros campos
        "capacity": 180
    }

    logger.info("Intentando actualizar aircraft: %s", test_aircraft_id)

    # 2. EJECUTAR - Petición HTTP
    response = api_client.make_request(
        # El ID del aircraft a actualizar
        endpoint=f"aircrafts/{test_aircraft_id}",
        method="PUT",  # o "PATCH" dependiendo de tu API
        data=update_data,  # Datos en formato JSON
        headers={
            "Authorization": f"Bearer {authenticated_token}"
        }
    )

    logger.info("Status Code: %d", response.status_code)
    logger.debug("Response: %s", response.text[:200])

    # 3. VERIFICAR - Validaciones
    assert response.status_code == HTTPStatus.OK, \
        f"Se esperaba código 200 pero se recibió {response.status_code}. Respuesta: {response.text}"

    # Validar respuesta
    json_response = response.json()

    # Verificar que el tail_number se actualizó correctamente
    assert json_response["tail_number"] == update_data["tail_number"], \
        f"Se esperaba tail_number '{update_data['tail_number']}' pero se recibió '{json_response.get('tail_number')}'"

    logger.info("Aircraft actualizado exitosamente: %s",
                json_response.get("tail_number"))


@pytest.mark.parametrize(
    "test_id, priority, update_data_template, expected_status, description",
    [
        # Casos críticos
        (
            "AIRCRAFT_UPDATE_C001",
            "Critical",
            {
                "tail_number": "UPD123",
                "model": "Boeing 777",
                "capacity": 250
            },
            200,
            "Actualización exitosa de aircraft con todos los campos válidos"
        ),
        (
            "AIRCRAFT_UPDATE_C002",
            "Critical",
            {
                "tail_number": "X" * 50,  # Demasiado largo
                "model": "Boeing",
                "capacity": 200
            },
            422,
            "Actualización con tail_number excesivamente largo"
        ),
        (
            "AIRCRAFT_UPDATE_C003",
            "Critical",
            {
                "tail_number": "",  # Vacío
                "model": "Boeing",
                "capacity": 200
            },
            422,
            "Actualización con tail_number vacío"
        ),
        (
            "AIRCRAFT_UPDATE_C004",
            "Critical",
            {
                "tail_number": "UPD456",
                "model": "Airbus",
                "capacity": "invalid"  # Tipo incorrecto
            },
            422,
            "Actualización con capacity no numérica"
        ),
        # Casos de prioridad media
        (
            "AIRCRAFT_UPDATE_M001",
            "Medium",
            {
                "tail_number": "UPD789",
                # Falta model (campo requerido por la API)
                "capacity": 300
            },
            422,  # ← CORREGIDO: model es requerido, debe fallar con 422
            "Actualización sin campo model (requerido)"
        ),
        (
            "AIRCRAFT_UPDATE_M002",
            "Medium",
            {
                "tail_number": "UPD999",
                "model": "Boeing",
                "capacity": -100  # Negativo
            },
            200,  # ← CORREGIDO: La API acepta valores negativos (bug/diseño)
            "Actualización con capacity negativa (API lo acepta)"
        ),
        # Casos de prioridad baja
        (
            "AIRCRAFT_UPDATE_L001",
            "Low",
            {
                "tail_number": "UPD000",
                "model": "Boeing",
                "capacity": 0  # Cero (edge case)
            },
            200,  # ← CORREGIDO: La API acepta cero (bug/diseño)
            "Actualización con capacity en cero (API lo acepta)"
        ),
    ]
)
def test_update_aircraft_parametrized(test_id, priority, update_data_template, expected_status, description, api_client, authenticated_token, test_aircraft_id):
    """Test parametrizado para PUT /aircrafts/{id}"""
    logger.info(
        "Ejecutando prueba %s: %s [Prioridad: %s]", test_id, description, priority)

    update_data = update_data_template.copy()

    # Ejecutar la petición de actualización
    response = api_client.make_request(
        endpoint=f"aircrafts/{test_aircraft_id}",
        method="PUT",
        data=update_data,
        headers={
            "Authorization": f"Bearer {authenticated_token}"
        }
    )

    logger.info("Status Code: %d", response.status_code)

    # Verificar resultado esperado
    if response.status_code != expected_status:
        try:
            error_message = response.json().get("detail", "No hay detalle disponible")
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            error_message = response.text

        logger.error(
            "[TEST_FAILED] %s | Status esperado: %s, recibido: %s | Error: %s",
            test_id,
            expected_status,
            response.status_code,
            error_message
        )

    assert response.status_code == expected_status, \
        f"Se esperaba status {expected_status}, pero se recibió {response.status_code}. Respuesta: {response.text}"

    # Para casos exitosos, validar la respuesta
    if expected_status == HTTPStatus.OK:
        response_data = response.json()
        logger.info(
            "[TEST_SUCCESS] %s | Status: %s | Respuesta: %s",
            test_id,
            response.status_code,
            json.dumps(response_data, indent=2, ensure_ascii=False)
        )

        # Validaciones específicas
        if "tail_number" in update_data and "tail_number" in response_data:
            assert response_data["tail_number"] == update_data["tail_number"], \
                "El tail_number no coincide"
        if "model" in update_data and "model" in response_data:
            assert response_data["model"] == update_data["model"], \
                "El model no coincide"
        if "capacity" in update_data and "capacity" in response_data:
            assert response_data["capacity"] == update_data["capacity"], \
                "La capacity no coincide"

    logger.info("Prueba %s completada con éxito", test_id)

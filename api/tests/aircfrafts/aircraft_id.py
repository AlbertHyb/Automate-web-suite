import logging
import time
import traceback
import json
import requests
import pytest
from api.pages.aircraft_page import AircraftPage

logger = logging.getLogger(__name__)

# --- Helper para operaciones de consulta por ID ---

def get_aircraft_by_id_request(aircraft_id, api_client, auth_headers=None):
    """Obtiene un avión por su ID usando el Page Object Model.

    Args:
      aircraft_id (str|int): identificador del avión
      api_client: instancia de ApiHelper
      auth_headers: headers de autenticación adicionales

    Returns:
      requests.Response

    Códigos esperados típicos:
      200 -> encontrado
      404 -> no existe
      401/403 -> problemas de auth
    """
    aircraft_page = AircraftPage(api_client)

    # Preparar headers con autenticación
    headers = {}
    if auth_headers:
        headers.update(auth_headers)

    start_time = time.time()

    # Validación mínima local del parámetro
    if aircraft_id is None or (isinstance(aircraft_id, str) and not aircraft_id.strip()):
        logger.error("[AIRCRAFT_GET_INVALID_PARAM] aircraft_id vacío o None")
        fake_response = requests.Response()
        fake_response.status_code = 400
        fake_response._content = json.dumps({
            "detail": "aircraft_id inválido (vacío o None)",
            "endpoint": "aircrafts/{aircraft_id}"
        }).encode('utf-8')
        return fake_response

    logger.debug(f"Enviando GET /aircrafts/{aircraft_id}")

    try:
        response = aircraft_page.get_aircraft_by_id(aircraft_id, headers=headers)
        duration = time.time() - start_time

        # Logging según el resultado
        if response.status_code == 200:
            try:
                body = response.json()
                preview = json.dumps(body, ensure_ascii=False)[:200]
            except Exception:
                preview = response.text[:200]
            logger.info(
                f"[AIRCRAFT_GET_SUCCESS] id={aircraft_id} status={response.status_code} t={duration:.3f}s preview={preview}"
            )
        elif response.status_code == 404:
            logger.warning(
                f"[AIRCRAFT_GET_NOT_FOUND] id={aircraft_id} status={response.status_code} t={duration:.3f}s"
            )
        elif response.status_code == 422:
            logger.warning(
                f"[AIRCRAFT_GET_VALIDATION_ERROR] id={aircraft_id} status={response.status_code} t={duration:.3f}s"
            )
        else:
            try:
                error_data = response.json()
                if isinstance(error_data, dict):
                    detail = error_data.get('detail', 'No detail provided')
                    body_repr = json.dumps(error_data, indent=2, ensure_ascii=False)
                else:
                    detail = 'Respuesta JSON no dict'
                    body_repr = str(error_data)
            except Exception:
                detail = 'Respuesta no JSON'
                body_repr = response.text[:422]
            logger.error(
                f"[AIRCRAFT_GET_ERROR] id={aircraft_id} status={response.status_code} t={duration:.3f}s detail={detail} body={body_repr}"
            )
        return response

    except Exception as e:
        duration = time.time() - start_time
        error_type = type(e).__name__
        logger.error(
            f"[AIRCRAFT_GET_EXCEPTION] id={aircraft_id} tipo={error_type} t={duration:.3f}s msg={str(e)} traza={traceback.format_exc()}"
        )
        fake_response = requests.Response()
        fake_response.status_code = 500
        fake_response._content = json.dumps({
            "detail": str(e),
            "error_type": error_type,
            "endpoint": f"aircrafts/{aircraft_id}"
        }).encode('utf-8')
        return fake_response


# --- Tests parametrizados ---

@pytest.mark.parametrize("scenario, expected_status", [
    ("valid", 200),
    ("not_found", 404),
    ("invalid_type", 404),
    ("negative_id", 404),
])
def test_get_aircraft_by_id(scenario, expected_status, api_client, auth_headers, aircraft_id):
    """Prueba parametrizada para GET /aircrafts/{aircraft_id} usando POM."""

    # Determinar el ID a usar según el escenario
    if scenario == "valid":
        aircraft_id_to_use = aircraft_id
    elif scenario == "not_found":
        aircraft_id_to_use = 999999999  # ID que no existe
    elif scenario == "invalid_type":
        aircraft_id_to_use = "abcxyz"   # ID no numérico
    elif scenario == "negative_id":
        aircraft_id_to_use = -10        # ID negativo

    # Ejecutar la prueba usando el helper
    response = get_aircraft_by_id_request(aircraft_id_to_use, api_client, auth_headers)

    # Verificar el resultado
    assert response.status_code == expected_status, (
        f"Fallo en el escenario {scenario}. Status esperado: {expected_status}, recibido: {response.status_code}."
    )

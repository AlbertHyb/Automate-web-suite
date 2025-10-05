import os
import json
import time
import requests
import pytest
import logging
import datetime
import uuid
from typing import Dict
from dotenv import load_dotenv
from api.api_helper import ApiHelper
from http import HTTPStatus


logger = logging.getLogger(__name__)

load_dotenv()

BASE_URL = "https://cf-automation-airline-api.onrender.com"


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="module")
def api_client(base_url):
    """Fixture centralizado para crear un cliente de API para las pruebas."""
    client = ApiHelper(base_url)

    if not client.is_service_up():
        pytest.skip("El servicio API no está disponible")
    logger.info("Servicio API disponible")

    return client


@pytest.fixture(scope="session")
def admin_token(base_url: str) -> str:
    username = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASS")

    login_data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "scope": "read write",
        "client_id": "test_client",
        "client_secret": "test_secret"
    }

    try:
        logger.info("Intentando login con usuario: %s", username)
        response = requests.post(
            f"{base_url}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=60  # Aumentado a 60s para cold starts de Render.com
        )
        logger.info("Login response (%s): %s",
                    response.status_code, response.text)

        if response.status_code != 200:
            pytest.fail("Error en login de admin: %s", response.text)

        token = response.json().get("access_token")
        if not token:
            pytest.fail("No se encontró el token en la respuesta")

        logger.info("Login de admin exitoso")
        return token

    except requests.Timeout:
        pytest.fail(
            f"Timeout al intentar hacer login (60s). La API en {base_url} puede estar dormida (cold start).")
    except requests.ConnectionError as e:
        pytest.fail(f"Error de conexión al intentar hacer login: {str(e)}")
    except Exception as e:
        pytest.fail("Error al obtener el token de admin: %s", str(e))


@pytest.fixture(scope="function")
def auth_headers(admin_token: str) -> Dict[str, str]:
    """Fixture que proporciona headers de autenticación con el token de admin."""
    return {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="session")
def authenticated_token(admin_token: str) -> str:
    """Alias para admin_token para compatibilidad con tests existentes."""
    return admin_token


# DESHABILITADO: Este hook causa bucles infinitos al re-ejecutar tests fallidos
# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     """Hook para generar reportes específicos cuando hay fallos"""
#     failed = bool(terminalreporter.stats.get("failed"))
#     if failed:
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         report_path = f"reports/failures_{timestamp}.html"
#
#         # Re-ejecutar las pruebas fallidas con reporte detallado
#         pytest.main([
#             "--html=" + report_path,
#             "--self-contained-html",
#             "--tb=long",
#             "--showlocals",
#             "--last-failed"
#         ])


@pytest.fixture(scope="module")
def test_user(admin_token) -> Dict:
    """Fixture para crear un usuario de prueba temporal."""
    user_data = {
        "email": f"alberto{int(time.time())}@example.com",
        "password": "TestPass123!",
        "full_name": "Test",
        "last_name": "User",
        "role": "passenger"
    }

    try:
        # Crear usuario usando el admin_token
        response = requests.post(
            f"{BASE_URL}/users",
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
            timeout=10
        )

        if response.status_code not in [200, 201]:
            pytest.fail(f"Error creando usuario de prueba: {response.text}")

        print(f"Usuario de prueba creado: {user_data['email']}")

        yield user_data

        # Cleanup - eliminar usuario después de las pruebas (opcional)
        # requests.delete(
        #     f"{BASE_URL}/users/{user_data['email']}",
        #     headers={"Authorization": f"Bearer {admin_token}"}
        # )

    except Exception as e:
        pytest.fail(f"Error en fixture test_user: {str(e)}")


@pytest.fixture(scope="function")
def create_aircraft(api_client, authenticated_token):
    """
    Fixture que CREA un aircraft y devuelve sus datos completos.
    Al finalizar el test, lo ELIMINA automáticamente.
    """
    # Generar datos únicos para el aircraft (máximo 10 caracteres)
    # Ejemplo: "T1A2B3" (6 caracteres)
    unique_id = f"T{uuid.uuid4().hex[:5].upper()}"

    aircraft_data = {
        "tail_number": unique_id,
        "model": "Boeing",
        "capacity": 400
    }

    logger.info("Creando aircraft de prueba: %s", unique_id)

    # CREAR el aircraft
    response = api_client.make_request(
        endpoint="aircrafts",
        method="POST",
        data=aircraft_data,
        headers={"Authorization": f"Bearer {authenticated_token}"}
    )

    assert response.status_code == HTTPStatus.CREATED, \
        f"Error al crear aircraft de prueba: {response.text}"

    created_aircraft = response.json()

    logger.info("Aircraft creado exitosamente con ID: %s",
                created_aircraft.get("id"))

    # Devolver el aircraft completo (con el ID generado por la base de datos)
    yield created_aircraft

    # CLEANUP: Eliminar después del test
    try:
        logger.info("Eliminando aircraft de prueba: %s",
                    created_aircraft.get("id"))
        api_client.make_request(
            endpoint=f"aircrafts/{created_aircraft['id']}",
            method="DELETE",
            headers={"Authorization": f"Bearer {authenticated_token}"}
        )
        logger.info("Aircraft eliminado correctamente")
    except Exception as e:
        logger.warning("Error al eliminar aircraft: %s", str(e))


@pytest.fixture(scope="function")
def test_aircraft_id(api_client, authenticated_token):
    """Fixture que crea un aircraft de prueba con ID único"""

    # Generar ID único para evitar conflictos (máximo 10 caracteres)
    # Ejemplo: "T1A2B3" (6 caracteres)
    unique_id = f"T{uuid.uuid4().hex[:5].upper()}"

    aircraft_data = {
        # ← Campo requerido por la API (máx 10 chars)
        "tail_number": unique_id,
        "model": "Boeing 747",
        "capacity": 400
    }

    response = api_client.make_request(
        endpoint="aircrafts",
        method="POST",
        data=aircraft_data,
        headers={"Authorization": f"Bearer {authenticated_token}"}
    )

    assert response.status_code == HTTPStatus.CREATED, \
        f"Error al crear aircraft de prueba: {response.text}"

    aircraft_id = response.json()["id"]

    yield aircraft_id

    # Cleanup: eliminar después del test
    try:
        api_client.make_request(
            endpoint=f"aircrafts/{aircraft_id}",
            method="DELETE",
            headers={"Authorization": f"Bearer {authenticated_token}"}
        )
    except Exception as e:
        print(f"Error al eliminar aircraft {aircraft_id}: {e}")


@pytest.fixture(scope="function")
def test_flight_id(api_client, authenticated_token, create_aircraft):

    # Obtener el aircraft_id del fixture create_aircraft
    aircraft_id = create_aircraft["id"]

    # Generar datos únicos para el flight
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    departure = now + timedelta(hours=2)
    arrival = departure + timedelta(hours=5)

    flight_data = {
        "aircraft_id": aircraft_id,
        "origin": "BOG",
        "destination": "MIA",
        "departure_time": departure.strftime("%Y-%m-%dT%H:%M:%S"),
        "arrival_time": arrival.strftime("%Y-%m-%dT%H:%M:%S"),
        "base_price": 250.50,
        "available_seats": 150
    }

    logger.info("Creando flight de prueba con aircraft_id: %s", aircraft_id)

    # CREAR el flight
    response = api_client.make_request(
        endpoint="flights",
        method="POST",
        data=flight_data,
        headers={"Authorization": f"Bearer {authenticated_token}"}
    )

    assert response.status_code == HTTPStatus.CREATED, \
        f"Error al crear flight de prueba: {response.text}"

    created_flight = response.json()
    flight_id = created_flight.get("id")

    logger.info("Flight creado exitosamente con ID: %s", flight_id)

    # Devolver el ID del flight
    yield flight_id

    # CLEANUP: Eliminar después del test
    try:
        logger.info("Eliminando flight de prueba: %s", flight_id)
        api_client.make_request(
            endpoint=f"flights/{flight_id}",
            method="DELETE",
            headers={"Authorization": f"Bearer {authenticated_token}"}
        )
        logger.info("Flight eliminado correctamente")
    except Exception as e:
        logger.warning("Error al eliminar flight: %s", str(e))





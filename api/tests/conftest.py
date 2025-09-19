import os
import pytest
from config.settings import Config
from api.api_helper import ApiHelper
import datetime
import requests
import time
from http import HTTPStatus
import logging
from datetime import datetime
from api.tests.airports.list_airports import fetch_data

# Configuración
config = Config()

BASE_URL = "https://cf-automation-airline-api.onrender.com"

# Configuración global de logging para todos los tests
# Usar ruta absoluta para la carpeta logs en la raíz del proyecto
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, 'error.log')

logging.basicConfig(
    level=logging.INFO,  # Guardar todos los niveles: DEBUG, INFO, WARNING, ERROR, CRITICAL
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
print(f"Ruta absoluta del log: {log_filename}")
#logger.debug("Mensaje de prueba DEBUG: validando creación de error.log en la ruta configurada.")
logger.info("Mensaje de prueba INFO: validando creación de error.log en la ruta configurada.")
logger.warning("Mensaje de prueba WARNING: validando creación de error.log en la ruta configurada.")
logger.error("Mensaje de prueba ERROR: validando creación de error.log en la ruta configurada.")
logger.critical("Mensaje de prueba CRITICAL: validando creación de error.log en la ruta configurada.")

@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL

@pytest.fixture(scope="module")
def api_client(base_url):
    """Fixture centralizado para crear un cliente de API para las pruebas."""
    api_client = ApiHelper(base_url)

    if not api_client.is_service_up():
        pytest.skip("El servicio API no está disponible")
    print("Servicio API disponible")

    return api_client

@pytest.fixture(scope="session")
def admin_token() -> str:
    creds = Config.get_auth_credentials()
    username = creds["username"]
    password = creds["password"]
    login_data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "scope": "read write",
        "client_id": "test_client",
        "client_secret": "test_secret"
    }

    try:
        print("\nIntentando login de admin...")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"Login response ({response.status_code}): {response.text}")

        if response.status_code != 200:
            pytest.fail(f"Error en login de admin: {response.text}")

        token = response.json().get("access_token")
        if not token:
            pytest.fail("No se encontró el token en la respuesta")

        print("Login de admin exitoso")
        return token

    except Exception as e:
        pytest.fail(f"Error al obtener el token de admin: {str(e)}")

@pytest.fixture(scope="function")
def test_user(api_client):
    """Crea un usuario de prueba único y retorna su user_id y token."""
    import time
    signup_data = Config.get_signup_status_data()
    unique_email = f"test_user_{int(time.time() * 1000)}@gmail.com"
    signup_data["email"] = unique_email
    response = api_client.make_request(
        endpoint="auth/signup",
        method="POST",
        data=signup_data
    )
    assert response.status_code in (200, 201), f"No se pudo crear usuario de prueba. Respuesta: {response.text}"
    user_id = response.json().get("uid")
    # Login para obtener el token
    login_data = {
        "username": unique_email,
        "grant_type": "password",
        "password": signup_data["password"],
        "scope": "read write",
        "client_id": "test_client",
        "client_secret": "test_secret"
    }

    login_response = api_client.make_request(
        endpoint="auth/login",
        method="POST",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        use_form_data=True
    )
    assert login_response.status_code == 200, f"No se pudo hacer login del usuario de prueba. Respuesta: {login_response.text}"
    token = login_response.json().get("access_token")
    return {
        "uid": user_id,
        "token": token,
        "email": unique_email,
        "password": signup_data["password"]
    }

@pytest.fixture(scope="session")
def ensure_test_user(base_url, test_user):
    """Registra el usuario de prueba si no existe."""
    signup_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    # Intentar registrar el usuario
    response = requests.post(
        f"{base_url}/auth/signup",
        json=signup_data,
        headers={"Content-Type": "application/json"}
    )
    # Si el usuario ya existe, la API puede devolver 400 o 409, lo ignoramos
    if response.status_code in (200, 201):
        print(f"Usuario de prueba registrado: {signup_data['email']}")
    elif response.status_code in (400, 409):
        print(f"Usuario de prueba ya existe: {signup_data['email']}")
    else:
        print(f"Error al registrar usuario de prueba: {response.status_code} {response.text}")
    yield

@pytest.fixture
def auth_signup(api_client):
    """Crea un usuario de prueba y retorna sus datos y token."""
    timestamp = int(time.time())
    email = f"fernandohz{timestamp}@gmail.com"
    password = "Cafe&Libro456?"
    full_name = "Fernando Hernandez"
    test_data = {
        "email": email,
        "password": password,
        "full_name": full_name
    }
    # Crear usuario
    signup_resp = api_client.make_request(
        method="POST",
        endpoint="auth/signup",
        data=test_data
    )
    assert signup_resp.status_code == HTTPStatus.CREATED
    user_id = signup_resp.json().get("id")

    # Login para obtener el token
    login_data = {
        "username": email,
        "password": password,
        "grant_type": "password",
        "scope": "read write",
        "client_id": "test_client",
        "client_secret": "test_secret"
    }
    login_resp = api_client.make_request(
        method="POST",
        endpoint="auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        use_form_data=True
    )
    assert login_resp.status_code == HTTPStatus.OK
    access_token = login_resp.json().get("access_token")

    return {
        "user_id": user_id,
        "access_token": access_token,
        "email": email,
        "password": password,
        "full_name": full_name
    }

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Hook para generar reportes específicos cuando hay fallos"""
    failed = bool(terminalreporter.stats.get("failed"))
    if failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"reports/failures_{timestamp}.html"

        # Re-ejecutar las pruebas fallidas con reporte detallado
        pytest.main([
            "--html=" + report_path,
            "--self-contained-html",
            "--tb=long",
            "--showlocals",
            "--last-failed"
        ])

@pytest.fixture
def static_airport():
    return {
        "id": 1,
        "name": "John F. Kennedy International Airport",
        "code": "JFK",
        "city": "New York",
        "country": "USA",
        "latitude": 40.6413,
        "longitude": -73.7781,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }

@pytest.fixture
def auth_headers(admin_token):
    return {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }




@pytest.fixture(scope="module")
def airport_test_data(api_client):
    """
    Fixture que proporciona datos de aeropuertos para las pruebas.
    Obtiene la lista de aeropuertos existentes y crea casos de prueba para validación.
    """
    # Obtener lista de aeropuertos
    list_response = fetch_data(skip=0, limit=30, api_client=api_client)

    if list_response.status_code != 200:
        pytest.skip("No se pudo obtener la lista de aeropuertos para las pruebas")

    airports = list_response.json()

    if not airports or len(airports) == 0:
        pytest.skip("No hay aeropuertos disponibles para las pruebas")

    # Registrar algunos aeropuertos disponibles para referencia
    logger.info(f"Aeropuertos disponibles para pruebas: {[a['iata_code'] for a in airports[:5]]}")

    # Crear un código IATA que definitivamente no existe
    invalid_iata = "ZZZ" if "ZZZ" not in [a["iata_code"] for a in airports] else "XXX"

    # Devolver los datos para las pruebas
    return {
        "airports": airports,
        "valid_iata": airports[0]["iata_code"],
        "invalid_iata": invalid_iata
    }
import os
import pytest
from config.settings import Config
from api.api_helper import ApiHelper
import datetime

# Configuración
config = Config()

BASE_URL = "https://cf-automation-airline-api.onrender.com"

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

@pytest.fixture
def test_user():
    return {
        "email": "testuser@example.com",
        "password": "testpassword"
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

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Hook para generar reportes específicos cuando hay fallos"""
    failed = bool(terminalreporter.stats.get("failed"))
    if failed:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"reports/failures_{timestamp}.html"

        # Re-ejecutar las pruebas fallidas con reporte detallado
        pytest.main([
            "--html=" + report_path,
            "--self-contained-html",
            "--tb=long",
            "--showlocals",
            "--last-failed"
        ])

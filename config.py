import os
import json
import time
import requests
import pytest
from typing import Dict
from dotenv import load_dotenv
from api.api_helper import ApiHelper
import datetime

# Cargar variables de entorno
load_dotenv()

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

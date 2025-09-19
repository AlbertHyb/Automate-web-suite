import os
import pytest
import requests
import json
import time
from http import HTTPStatus
from jsonschema import validate, ValidationError
from test.api.schemas.list_user_get import list_users_success_schema


class ApiHelper:
    def __init__(self, base_url):
        self.base_url = base_url
        # Puedes implementar aquí inicialización de sesión o headers si es necesario
    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params, headers=headers)
        return response

    def post(self, endpoint, data=None, headers=None, use_form_data=False):
        url = f"{self.base_url}{endpoint}"
        if use_form_data:
            response = requests.post(url, data=data, headers=headers)
        else:
            response = requests.post(url, json=data, headers=headers)
        return response

    def make_request(self, endpoint, method="GET", data=None, params=None, headers=None, use_form_data=False):
        url = f"{self.base_url}{endpoint}"
        method = method.upper()
        if method == "GET":
            return requests.get(url, params=params, headers=headers)
        elif method == "POST":
            if use_form_data:
                return requests.post(url, data=data, headers=headers)
            else:
                return requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            if use_form_data:
                return requests.put(url, data=data, headers=headers)
            else:
                return requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            return requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Método HTTP no soportado: {method}")

@pytest.fixture(scope="module")
def api_client(base_url):
    """Fixture para crear un cliente de API para las pruebas de autenticación."""
    # La URL base se pasa desde la fixture en conftest.py
    return ApiHelper(base_url)

@pytest.fixture(scope="module")
def auth_token(api_client):
    """Fixture para obtener un token de autenticación válido. Si el usuario no existe, lo crea."""
    username = os.environ.get("ADMIN_USER")
    password = os.environ.get("ADMIN_PASS")
    if not username or not password:
        raise RuntimeError("ADMIN_USER o ADMIN_PASS no están definidos en las variables de entorno.")
    login_data = {
        "username": username,
        "password": password
    }
    # Intentar registrar el usuario primero
    try:
        signup_response = api_client.make_request(
            endpoint="/auth/signup",
            method="POST",
            data=login_data,
            use_form_data=True
        )
        # Si el usuario ya existe, puede devolver 409 o un mensaje de error, lo ignoramos
    except Exception:
        pass
    # Ahora intentar loguearse
    response = api_client.make_request(
        endpoint="/auth/login",
        method="POST",
        data=login_data,
        use_form_data=True
    )
    assert response.status_code == HTTPStatus.OK, f"Error al obtener el token de autenticación: {response.status_code}, {response.text}"
    return response.json().get("access_token")

@pytest.fixture(scope="module", autouse=True)
def server_status_and_response_time(api_client):
    """Fixture para verificar si el servidor responde y medir el tiempo de respuesta, mostrando el mensaje de respuesta."""
    # Usar un endpoint seguro para health check, por ejemplo /users (GET)
    start_time = time.time()
    try:
        response = api_client.get("/users")
        response_time = time.time() - start_time
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except Exception:
            print(f"Response: {response.text}")
        print(f"Tiempo de respuesta del servidor: {response_time:.3f} segundos")
    except Exception as e:
        response_time = time.time() - start_time
        print(f"El servicio API no está disponible en este momento. Tiempo de respuesta: {response_time:.3f} segundos")
        print(f"Error: {e}")

@pytest.mark.usefixtures("api_client")
class TestListUsers:
    def test_list_users_success(self, api_client, auth_token):
        """Test para obtener la lista de usuarios con parámetros skip y limit."""
        params = {
            "skip": 0,
            "limit": 10
        }
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        response = api_client.get("/users", params=params, headers=headers)
        # Verificar el código HTTP 200
        assert response.status_code == HTTPStatus.OK
        # Validar que el contenido sea JSON y obtener la respuesta
        json_response = None
        try:
            json_response = response.json()
        except ValueError:
            pytest.fail("La respuesta no es un JSON válido")
        # Mostrar la lista de usuarios en formato JSON legible
        print("\nLista de usuarios registrados:")
        print(json.dumps(json_response, indent=2, ensure_ascii=False))
        # Validar el esquema JSON de la respuesta
        try:
            validate(instance=json_response, schema=list_users_success_schema)
        except ValidationError as e:
            pytest.fail(f"El esquema JSON no es válido: {e}")

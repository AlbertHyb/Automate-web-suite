import json
import pytest
import requests
import time
from http import HTTPStatus
from jsonschema import validate, ValidationError
from test.api.schemas.user_me_get_schema import user_me_get_schema
from config.settings import Config


class ApiHelper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        return requests.get(url, headers=headers)

    def post(self, endpoint, data=None, headers=None, use_form_data=False):
        url = f"{self.base_url}{endpoint}"
        if use_form_data:
            response = requests.post(url, data=data, headers=headers)
        else:
            response = requests.post(url, json=data, headers=headers)
        return response


def medir_tiempo_respuesta(api, endpoint, headers=None):
    inicio = time.time()
    response = api.get(endpoint, headers=headers)
    fin = time.time()
    tiempo = fin - inicio
    print(f"Tiempo de respuesta para {endpoint}: {tiempo:.4f} segundos")
    return response, tiempo


# Test para el endpoint /users/me
def test_get_users_me(admin_token):
    base_url = Config.get_base_url()
    api = ApiHelper(base_url)
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Accept": "application/json"
    }
    response, tiempo = medir_tiempo_respuesta(api, "/users/me", headers=headers)

    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Respuesta JSON:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception:
        print(f"Respuesta no es JSON: {response.text}")
        pytest.fail("La respuesta no es un JSON válido")

    if response.status_code != HTTPStatus.OK:
        pytest.fail(
            f"Se esperaba código 200 pero se recibió {response.status_code}.\n"
            f"URL: {response.url}\n"
            f"Headers: {headers}\n"
            f"Respuesta: {response.text}"
        )

    try:
        validate(instance=data, schema=user_me_get_schema)
    except ValidationError as e:
        pytest.fail(f"La respuesta JSON no cumple el esquema esperado: {e}")

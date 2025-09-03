import pytest
import requests
from jsonschema import validate, ValidationError
from http import HTTPStatus
from config.settings import Config
from config.constants import ENDPOINTS
from test.api.schemas.airport_schemas import airport_schema


def test_create_airport_schema(static_airport):
    """Test para verificar que la respuesta del endpoint de creación de aeropuerto
    cumple con el esquema JSON esperado"""

    try:
        validate(instance=static_airport, schema=airport_schema)
        print("El esquema del aeropuerto es válido")
    except ValidationError as e:
        pytest.fail(f"Error de validación del esquema: {e.message}")
    except Exception as e:
        pytest.fail(f"Error inesperado al validar el esquema: {str(e)}")


def test_get_all_airports(static_airport, auth_headers):
    """Test para verificar la obtención de todos los aeropuertos"""

    try:
        response = requests.get(
            f"{Config.get_base_url()}{ENDPOINTS['AIRPORTS']}",
            headers=auth_headers,
            timeout=Config.get_request_timeout()
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")

        # Verificar el código de estado
        assert response.status_code == HTTPStatus.OK, f"Expected 200, got {response.status_code}"

        # Verificar que la respuesta es JSON válido
        airports = response.json()
        # Verificar que la respuesta es una lista
        assert isinstance(airports, list), f"La respuesta debería ser una lista, pero es {type(airports)}"

        # Verificar que la lista no está vacía
        assert len(airports) > 0, "La lista de aeropuertos no debería estar vacía"

        print(f"Se encontraron {len(airports)} aeropuertos")

        # Verificar que cada aeropuerto cumple con el esquema
        for i, airport in enumerate(airports):
            try:
                validate(instance=airport, schema=airport_schema)
            except ValidationError as e:
                pytest.fail(f"El aeropuerto en la posición {i} no cumple con el esquema: {e.message}")

        print("Todos los aeropuertos cumplen con el esquema")

    except requests.RequestException as e:
        pytest.fail(f"Error en la petición HTTP: {str(e)}")
    except ValueError as e:
        pytest.fail(f"La respuesta no es JSON válido: {str(e)}")
    except Exception as e:
        pytest.fail(f"Error inesperado: {str(e)}")
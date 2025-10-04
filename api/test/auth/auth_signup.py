import pytest
import time
from http import HTTPStatus
from jsonschema import validate, ValidationError
from api.api_helper import ApiHelper
from api.schemas.signup_schemas import signup_success_schema



def test_user_registration_successful(api_client):
    """Test para verificar el registro exitoso de un usuario"""
    timestamp = int(time.time())
    test_data = {
        "email": f"albert{timestamp}@gmail.com",
        "password": "N1!W0TF$5p6Q",  # Usar una contraseña que cumpla los requisitos de la API
        "full_name": "Albert"
    }

    # Realizar la petición POST usando el helper
    response = api_client.make_request(
        endpoint="auth/signup",
        method="POST",
        data=test_data
    )

    # Verificar el código de estado
    assert response.status_code == HTTPStatus.CREATED, \
        f"Se esperaba 201 pero se recibió {response.status_code}. Respuesta: {response.text}"

    # Debug: Imprimir información detallada
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Response Text: {response.text}")

    # Si la respuesta es JSON, intentar parsearla
    try:
        print(f"Response JSON: {response.json()}")
    except:
        print("La respuesta no es JSON válido")

    response_data = response.json()

    # Validar el esquema de la respuesta para asegurar que la estructura es correcta
    try:
        validate(instance=response_data, schema=signup_success_schema)
    except ValidationError as e:
        pytest.fail(f"El esquema de la respuesta no es válido: {e}")
    except Exception as e:
        pytest.fail(f"Error inesperado al validar esquema: {e}")

    # Verificar que los datos específicos coincidan con lo enviado
    assert response_data["email"] == test_data["email"]
    assert response_data["full_name"] == test_data["full_name"]


def test_user_registration_invalid_email(api_client):
    """Test para verificar el manejo de email inválido"""
    test_data = {
        "email": "albert@gmail",
        "password": "t7O331\a{m<&",
        "full_name": "Albert"
    }

    response = api_client.make_request(
        endpoint="auth/signup", method="POST", data=test_data)

    # Verificar el código de estado para un email inválido
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, \
        f"Se esperaba 422 pero se recibió {response.status_code}. Respuesta: {response.text}"

    response_data = response.json()
    assert "detail" in response_data, "La respuesta no contiene el campo 'detail'"

import json
import pytest
from http import HTTPStatus
from jsonschema import validate
from api.schemas.login_schemas import user_login_success_schema, user_login_error_schema


def test_service_status(api_client):
    """Verifica que el servicio esté disponible antes de ejecutar las pruebas."""
    if api_client.is_service_up():
        print("El servicio API está funcionando correctamente")
    else:
        pytest.fail("El servicio API no está disponible")


def test_user_login_successful(api_client, test_user):
    """Test para verificar el login exitoso de un usuario."""
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
        "grant_type": "password",
        "scope": "read write"
    }

    print(f"\nIntentando login con datos: {json.dumps(login_data, indent=2)}")
    response = api_client.make_request(
        endpoint="auth/login",
        method="POST",
        data=login_data,
        use_form_data=True
    )

    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception:
        print(f"Response: {response.text}")

    assert response.status_code == HTTPStatus.OK, \
        f"Se esperaba código 200 pero se recibió {response.status_code}. Respuesta: {response.text}"

    # Validar respuesta
    json_response = response.json()
    validate(instance=json_response, schema=user_login_success_schema)

    # Validaciones específicas del token
    assert json_response["token_type"].lower(
    ) == "bearer", "El token_type no es 'bearer'"
    assert len(json_response["access_token"]) > 0, "Token vacío"

    print(f"Login exitoso para: {login_data['username']}")


def test_login_invalid_credentials(api_client):
    """Test para verificar el manejo de credenciales inválidas."""
    invalid_login = {
        "username": "noexiste@test.com",
        "password": "contraseña_incorrecta",
        "grant_type": "password"
    }

    print(
        f"\nIntentando login con credenciales inválidas: {json.dumps(invalid_login, indent=2)}")
    response = api_client.make_request(
        endpoint="auth/login",
        method="POST",
        data=invalid_login,
        use_form_data=True
    )

    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception:
        print(f"Response: {response.text}")

    assert response.status_code == HTTPStatus.UNAUTHORIZED, \
        f"Se esperaba código 401 pero se recibió {response.status_code}"

    print("Validación de credenciales inválidas correcta")


def test_login_missing_fields(api_client):
    """Test para verificar el manejo de campos faltantes."""
    incomplete_data = {
        "username": "test@example.com"
        # Falta password y grant_type intencionalmente
    }

    print(
        f"\nIntentando login con campos faltantes: {json.dumps(incomplete_data, indent=2)}")
    response = api_client.make_request(
        endpoint="auth/login",
        method="POST",
        data=incomplete_data,
        use_form_data=True
    )

    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception:
        print(f"Response: {response.text}")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    json_response = response.json()
    validate(instance=json_response, schema=user_login_error_schema)

    # Verificar campos faltantes
    error_fields = [error["loc"][1]
                    for error in json_response["detail"] if len(error["loc"]) > 1]
    assert "password" in error_fields, "No se reportó error por falta de password"

    print("Validación de campos requeridos correcta")


def test_login_invalid_format(api_client):
    """Test para verificar el manejo de datos con formato inválido."""
    invalid_format = {
        "username": "not_an_email",
        "password": "123",  # Contraseña muy corta
        "grant_type": "invalid_grant"
    }

    print(
        f"\nIntentando login con formato inválido: {json.dumps(invalid_format, indent=2)}")
    response = api_client.make_request(
        endpoint="auth/login",
        method="POST",
        data=invalid_format,
        use_form_data=True
    )

    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception:
        print(f"Response: {response.text}")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    json_response = response.json()
    validate(instance=json_response, schema=user_login_error_schema)

    print("Validación de formato de datos correcta")

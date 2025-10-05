import json
import pytest
from http import HTTPStatus
from jsonschema import validate
from api.schemas.login_schemas import user_login_success_schema, user_login_error_schema
import logging

logger = logging.getLogger(__name__)


def test_service_status(api_client):
    """Verifica que el servicio esté disponible antes de ejecutar las pruebas."""
    if api_client.is_service_up():
        logger.info("El servicio API está funcionando correctamente")
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

    logger.info("Intentando login con usuario: %s", login_data['username'])
    response = api_client.make_request(
        endpoint="auth/login",
        method="POST",
        data=login_data,
        use_form_data=True
    )

    logger.info("Status Code: %d", response.status_code)
    logger.debug("Response: %s", response.text[:200])

    assert response.status_code == HTTPStatus.OK, \
        f"Se esperaba código 200 pero se recibió {response.status_code}. Respuesta: {response.text}"

    # Validar respuesta
    json_response = response.json()
    validate(instance=json_response, schema=user_login_success_schema)

    # Validaciones específicas del token
    assert json_response["token_type"].lower(
    ) == "bearer", "El token_type no es 'bearer'"
    assert len(json_response["access_token"]) > 0, "Token vacío"

    logger.info("Login exitoso para: %s", login_data['username'])


@pytest.mark.parametrize("username,password,expected_status,test_id", [
    ("noexiste@test.com", "wrongpass123", HTTPStatus.UNAUTHORIZED, "invalid_user"),
    ("valid@test.com", "wrongpass", HTTPStatus.UNAUTHORIZED, "invalid_password"),
    ("", "password123", HTTPStatus.UNPROCESSABLE_ENTITY, "empty_username"),
    ("test@test.com", "", HTTPStatus.UNPROCESSABLE_ENTITY, "empty_password"),
    ("not_an_email", "pass123", HTTPStatus.UNAUTHORIZED, "invalid_email_format"),
], ids=lambda x: x[3] if isinstance(x, tuple) and len(x) > 3 else str(x))


def test_login_invalid_scenarios(api_client, username, password, expected_status, test_id):
    """Test parametrizado para diferentes escenarios de login inválido."""
    login_data = {
        "username": username,
        "password": password,
        "grant_type": "password"
    }

    logger.info("Test caso: %s - username=%s", test_id, username)
    response = api_client.make_request(
        endpoint="auth/login",
        method="POST",
        data=login_data,
        use_form_data=True
    )

    logger.info("Status esperado: %d, recibido: %d",
                expected_status, response.status_code)

    assert response.status_code == expected_status, \
        f"Caso '{test_id}': esperaba {expected_status}, recibió {response.status_code}. Response: {response.text}"


@pytest.mark.parametrize("missing_field,data,expected_status", [

    # Caso 1: Falta password
    ("password", {"username": "aquino@example.com",
     "grant_type": "password"}, HTTPStatus.UNPROCESSABLE_ENTITY),

    # Caso 2: Falta username
    ("username", {"password": "5ZBJ2q0]erp1",
     "grant_type": "password"}, HTTPStatus.UNPROCESSABLE_ENTITY),

    # Caso 3: Falta grant_type
    ("grant_type", {"username": "aquino@example.com",
     "password": "5ZBJ2q0]erp1"}, HTTPStatus.UNAUTHORIZED),
], ids=["missing_password", "missing_username", "missing_grant_type"])
def test_login_missing_required_fields(api_client, missing_field, data, expected_status):
    logger.info("Probando login sin campo: %s", missing_field)

    response = api_client.make_request(
        endpoint="auth/login",
        method="POST",
        data=data,
        use_form_data=True
    )

    logger.info("Status Code: %d", response.status_code)

    assert response.status_code == expected_status, \
        f"Esperaba {expected_status} al faltar '{missing_field}', recibió {response.status_code}"

    json_response = response.json()

    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        validate(instance=json_response, schema=user_login_error_schema)

    # Verificar que el error mencione el campo faltante
        error_fields = [error["loc"][-1] for error in json_response["detail"]]
        assert missing_field in error_fields, \
            f"El error no menciona el campo faltante '{missing_field}'. Errores: {error_fields}"

    else:
        # Para 401, solo verificar que hay un mensaje de error
        assert "detail" in json_response

    logger.info("Validación correcta para campo faltante: %s", missing_field)


@pytest.mark.parametrize("grant_type,expected_status", [
    ("password", HTTPStatus.UNAUTHORIZED),      # Válido pero creds incorrectas
    ("client_credentials", HTTPStatus.UNAUTHORIZED),  # Otro grant type válido
    ("invalid_grant", HTTPStatus.UNAUTHORIZED),  # Grant type inválido
    ("", HTTPStatus.UNPROCESSABLE_ENTITY),      # Grant type vacío

], ids=["valid_password", "client_credentials", "invalid_grant", "empty_grant"])


def test_login_grant_type_variations(api_client, grant_type, expected_status):
    """Test parametrizado para diferentes tipos de grant_type."""
    login_data = {
        "username": "test@example.com",
        "password": "wrongpass",
    }

    if grant_type is not None:
        login_data["grant_type"] = grant_type

    logger.info("Probando grant_type: '%s'", grant_type)

    response = api_client.make_request(
        endpoint="auth/login",
        method="POST",
        data=login_data,
        use_form_data=True
    )

    logger.info("Grant type '%s' - Status: %d (esperado: %d)",
                grant_type, response.status_code, expected_status)

    assert response.status_code == expected_status, \
        f"Grant type '{grant_type}': esperaba {expected_status}, recibió {response.status_code}"

# Validaciones adicionales para ciertos códigos de estado
    json_response = response.json()
    assert "detail" in json_response, "La respuesta debe contener un campo 'detail'"


    logger.info("Validación correcta para grant_type: '%s'", grant_type)


def test_login_success_schema_validation(api_client, test_user):
    """Validación estricta del schema de respuesta exitosa."""
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
        "grant_type": "password",
        "scope": "read write"
    }

    response = api_client.make_request(
        endpoint="auth/login",
        method="POST",
        data=login_data,
        use_form_data=True
    )

    assert response.status_code == HTTPStatus.OK
    json_response = response.json()

    # Validación con jsonschema
    validate(instance=json_response, schema=user_login_success_schema)

    # Validaciones adicionales de negocio
    assert "access_token" in json_response
    assert "token_type" in json_response
    assert json_response["token_type"].lower() == "bearer"
    assert isinstance(json_response["access_token"], str)
    # Token mínimo de longitud razonable
    assert len(json_response["access_token"]) > 20

    logger.info("Schema de login exitoso validado correctamente")


def test_login_error_schema_validation(api_client):
    """Validación estricta del schema de respuesta de error."""
    invalid_login = {
        "username": "test@test.com"
        # Falta password intencionalmente
    }

    response = api_client.make_request(
        endpoint="auth/login",
        method="POST",
        data=invalid_login,
        use_form_data=True
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    json_response = response.json()

    # Validación con jsonschema
    validate(instance=json_response, schema=user_login_error_schema)

    # Validaciones adicionales
    assert "detail" in json_response
    assert isinstance(json_response["detail"], list)
    assert len(json_response["detail"]) > 0

    # Validar estructura de cada error
    for error in json_response["detail"]:
        assert "loc" in error
        assert "msg" in error
        assert "type" in error

    logger.info("Schema de error validado correctamente")

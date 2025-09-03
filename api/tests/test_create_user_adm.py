import json
import pytest
from http import HTTPStatus
from jsonschema import validate, ValidationError
from test.api.schemas.create_user_adm_schemas import create_user_adm_success_schema, create_user_adm_error_schema

# Datos constantes para usuario admin de prueba
TEST_ADMIN_DATA = {
    "email": "test.admin@example.com",
    "password": "TestAdmin123!",
    "full_name": "Test Administrator",
    "role": "admin"
}


@pytest.fixture(scope="module")
def admin_api_client(api_client, admin_token):
    """Fixture que proporciona un cliente API con token de admin"""
    api_client.set_token(admin_token)
    return api_client


def test_service_status(api_client):
    """Verifica que el servicio esté disponible antes de ejecutar las pruebas."""
    if api_client.is_service_up():
        print("El servicio API está funcionando correctamente")
    else:
        pytest.fail("El servicio API no está disponible")


def test_create_user_as_admin(admin_api_client):
    """Test para verificar la creación exitosa de un usuario admin"""
    print(f"\nIntentando crear usuario admin con datos: {json.dumps(TEST_ADMIN_DATA, indent=2)}")

    # Verificar si el usuario ya existe
    try:
        check_response = admin_api_client.make_request(
            endpoint=f"users/{TEST_ADMIN_DATA['email']}",
            method="GET"
        )

        if check_response.status_code == HTTPStatus.OK:
            print(f"ℹ️ El usuario admin {TEST_ADMIN_DATA['email']} ya existe")
            print("ℹ️ Intentando eliminar el usuario existente...")

            delete_response = admin_api_client.make_request(
                endpoint=f"users/{TEST_ADMIN_DATA['email']}",
                method="DELETE"
            )

            if delete_response.status_code in [HTTPStatus.OK, HTTPStatus.NO_CONTENT]:
                print("Usuario existente eliminado correctamente")
            else:
                pytest.skip(f"No se pudo eliminar el usuario existente: {delete_response.text}")
    except Exception as e:
        print(f"ℹ️ Error al verificar usuario existente: {str(e)}")

    # Crear el usuario admin
    response = admin_api_client.make_request(
        endpoint="users",
        method="POST",
        data=TEST_ADMIN_DATA
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2) if response.text else 'No response body'}")

    # Manejar diferentes códigos de respuesta
    if response.status_code == HTTPStatus.BAD_REQUEST:
        error_msg = response.json().get("detail", "")
        if "Email already registered" in error_msg:
            pytest.skip(f"No se puede crear el usuario admin: {error_msg}")
        else:
            pytest.fail(f"Error inesperado: {error_msg}")

    assert response.status_code == HTTPStatus.CREATED, \
        f"Se esperaba código 201 pero se recibió {response.status_code}. Respuesta: {response.text}"

    try:
        validate(instance=response.json(), schema=create_user_adm_success_schema)
        print("Usuario administrador creado exitosamente")
    except ValidationError as err:
        pytest.fail(f"El esquema de respuesta no es válido: {err}")


def test_create_user_as_admin_validation_error(admin_api_client):
    """Test para verificar el manejo de errores de validación"""
    invalid_admin_data = {
        "email": "not-an-email",
        "password": "",
        "full_name": "",
        "role": "unknown_role"  # Rol inválido
    }

    print(f"\nIntentando crear usuario admin con datos inválidos: {json.dumps(invalid_admin_data, indent=2)}")
    response = admin_api_client.make_request(
        endpoint="users",
        method="POST",
        data=invalid_admin_data
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2) if response.text else 'No response body'}")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, \
        f"Se esperaba código 422 pero se recibió {response.status_code}"

    try:
        validate(instance=response.json(), schema=create_user_adm_error_schema)
        print("Validación de errores correcta")
    except ValidationError as err:
        pytest.fail(f"El esquema de error no es válido: {err}")

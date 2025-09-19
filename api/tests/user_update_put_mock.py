import pytest
from unittest.mock import Mock, patch
from http import HTTPStatus
from jsonschema import validate, ValidationError
from api.api_helper import ApiHelper
from api.schemas.user_update_put_schema import user_update_put_schema


"""
Test alternativo usando mocks para validar la lógica mientras la API está caída
Ejecutar: pytest api/tests/user_update_put_mock.py -v
"""


class TestUpdateUserMock:
    """Suite de pruebas MOCK para el endpoint PUT /users/{user_id}"""

    @patch('api.api_helper.requests.put')
    def test_update_user_success_mock(self, mock_put):
        """Prueba exitosa de actualización de usuario usando mocks."""

        # Configurar el mock para simular una respuesta exitosa
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "uid": "usr-12345",
            "email": "user@example.com",
            "full_name": "string"
        }
        mock_put.return_value = mock_response

        # Datos de actualización
        update_data = {
            "email": "user@example.com",
            "password": "string",
            "full_name": "string"
        }

        # Crear cliente API y hacer la petición
        api_client = ApiHelper("https://mock-api.com")
        headers = {"Authorization": "Bearer mock_token"}

        response = api_client.make_request(
            endpoint="users/usr-12345",
            method="PUT",
            data=update_data,
            headers=headers
        )

        # Validaciones
        assert response.status_code == HTTPStatus.OK

        # Validar que se llamó con los parámetros correctos
        mock_put.assert_called_once()
        call_args = mock_put.call_args
        assert "users/usr-12345" in call_args[1]['url']
        assert call_args[1]['json'] == update_data
        assert "Authorization" in call_args[1]['headers']

        # Validar el schema de respuesta
        try:
            validate(instance=response.json(), schema=user_update_put_schema)
        except ValidationError as e:
            pytest.fail(f"Response JSON no cumple con el schema: {e.message}")

        # Validar contenido de la respuesta
        body = response.json()
        assert body["uid"] == "usr-12345"
        assert body["email"] == update_data["email"]
        assert body["full_name"] == update_data["full_name"]

        print("Test mock exitoso - La lógica del test es correcta")

    @patch('api.api_helper.requests.put')
    def test_update_user_forbidden_mock(self, mock_put):
        """Prueba de actualización con usuario sin permisos."""

        # Configurar el mock para simular un error 403
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = '{"detail":"Forbidden"}'
        mock_put.return_value = mock_response

        update_data = {
            "email": "user@example.com",
            "password": "string",
            "full_name": "string"
        }

        api_client = ApiHelper("https://mock-api.com")
        headers = {"Authorization": "Bearer invalid_token"}

        response = api_client.make_request(
            endpoint="users/usr-12345",
            method="PUT",
            data=update_data,
            headers=headers
        )

        # Validar que maneja correctamente el error 403
        assert response.status_code == 403
        assert "Forbidden" in response.text

        print("Test de error 403 exitoso - El manejo de errores es correcto")

if __name__ == "__main__":
    # Ejecutar los tests directamente
    import sys
    sys.exit(pytest.main([__file__, "-v"]))

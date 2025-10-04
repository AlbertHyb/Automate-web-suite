import pytest
from http import HTTPStatus
from jsonschema import validate, ValidationError
from api.schemas.user_update_put_schema import user_update_put_schema


class TestUpdateUser:
    """Suite de pruebas para el endpoint PUT /users/{user_id}"""

    def test_update_user_success(self, api_client, admin_token):
        """Prueba exitosa de actualización de usuario usando admin token."""
        # Usar un user_id fijo conocido o el del admin
        admin_user_id = "usr-85aabee8"  # Extraído del token JWT del admin

        update_data = {
            "email": "user@example.com",
            "password": "string",
            "full_name": "string"
        }

        headers = {"Authorization": f"Bearer {admin_token}"}
        response = api_client.make_request(
            endpoint=f"users/{admin_user_id}",
            method="PUT",
            data=update_data,
            headers=headers
        )

        # Validaciones
        assert response.status_code == HTTPStatus.OK, f"Error: {response.text}"

        try:
            validate(instance=response.json(), schema=user_update_put_schema)
        except ValidationError as e:
            pytest.fail(f"Response JSON no cumple con el schema: {e.message}")

        body = response.json()
        assert body["uid"] == admin_user_id
        assert body["email"] == update_data["email"]
        assert body["full_name"] == update_data["full_name"]

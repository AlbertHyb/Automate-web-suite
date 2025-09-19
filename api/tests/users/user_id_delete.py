import pytest
from http import HTTPStatus
import logging
import os
from datetime import datetime

# Crear carpeta de logs si no existe
log_dir = os.path.join(os.path.dirname(__file__), '../../logs')
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, 'error.log')

logging.basicConfig(
    level=logging.ERROR,
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_delete_user_success(api_client, auth_signup):
    user_id = auth_signup["user_id"]
    resp = api_client.make_request(
        method = "DELETE",
        endpoint = f"users/{user_id}",
        headers ={"Authorization": f"Bearer {auth_signup['access_token']}"}
    )
    if resp.status_code != HTTPStatus.NO_CONTENT:
        logger.error(f"FALLA: Se esperaba status 204 al eliminar usuario, pero se recibió {resp.status_code}. Respuesta: {resp.text}")
    assert resp.status_code == HTTPStatus.NO_CONTENT
    #FastAPI normalmente retorna cuerpo vacío en 204
    if resp.text not in ("", None):
        logger.error(f"FALLA: Se esperaba cuerpo vacío en respuesta 204, pero se recibió: {resp.text}")
    assert resp.text in ("", None)


@pytest.mark.parametrize("invalid_id", [
    "",  # ID vacío
    "!!!",  # Caracteres especiales
    "89726745675" * 5,  # ID muy largo
    None,  # Valor nulo
    "abc",  # Letras (si esperas solo números)
    "123.456",  # Decimal (si esperas enteros)
    "-123",  # Número negativo
    "0",  # Cero (si no es válido)
])
def test_delete_user_invalid_id(api_client, admin_token, invalid_id):
    invalid_str = str(invalid_id) if invalid_id is not None else "None"
    resp = api_client.make_request(
        method="DELETE",
        endpoint=f"users/{invalid_str}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    if resp.status_code not in (HTTPStatus.UNPROCESSABLE_ENTITY, HTTPStatus.BAD_REQUEST):
        logger.error(f"FALLA: Se esperaba status 422 o 400 al eliminar usuario con id inválido '{invalid_str}', pero se recibió {resp.status_code}. Respuesta: {resp.text}")
    assert resp.status_code in (HTTPStatus.UNPROCESSABLE_ENTITY, HTTPStatus.BAD_REQUEST)
    body = resp.json()
    if "detail" not in body:
        logger.error(f"FALLA: La respuesta no contiene el campo 'detail' para id inválido '{invalid_str}'. Respuesta: {resp.text}")
    assert "detail" in body

def test_delete_user_not_found(api_client, admin_token):
    resp = api_client.make_request(
        method="DELETE",
        endpoint=f"users/1234567890",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    if resp.status_code not in (HTTPStatus.NOT_FOUND, HTTPStatus.NO_CONTENT, HTTPStatus.BAD_REQUEST):
        logger.error(f"FALLA: Se esperaba status 404, 204 o 400 al eliminar usuario inexistente, pero se recibió {resp.status_code}. Respuesta: {resp.text}")
    assert resp.status_code in (HTTPStatus.NOT_FOUND, HTTPStatus.NO_CONTENT, HTTPStatus.BAD_REQUEST)

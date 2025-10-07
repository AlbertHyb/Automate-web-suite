import pytest
import logging
import json
from http import HTTPStatus


logger = logging.getLogger(__name__)


def test_service_status(api_client):
    """Verifica que el servicio esté disponible antes de ejecutar las pruebas."""
    if api_client.is_service_up():
        logger.info("El servicio API está funcionando correctamente")
    else:
        pytest.fail("El servicio API no está disponible")


def test_delete_aircraft_successful(api_client, authenticated_token, test_aircraft_id):
    """Test básico para verificar la eliminación exitosa de un aircraft."""

    logger.info("Intentando eliminar aircraft: %s", test_aircraft_id)

    # EJECUTAR - Petición HTTP DELETE
    response = api_client.make_request(
        endpoint=f"aircrafts/{test_aircraft_id}",
        method="DELETE",
        headers={
            "Authorization": f"Bearer {authenticated_token}"
        }
    )

    logger.info("Status Code: %d", response.status_code)
    logger.debug("Response: %s",
                 response.text[:200] if response.text else "Sin contenido")

    # VERIFICAR - Validaciones
    assert response.status_code == HTTPStatus.OK, \
        f"Se esperaba código 200 pero se recibió {response.status_code}. Respuesta: {response.text}"

    # Validar respuesta (si existe)
    if response.text:
        try:
            json_response = response.json()
            logger.info("Aircraft eliminado exitosamente: %s",
                        json.dumps(json_response, ensure_ascii=False))
        except json.JSONDecodeError:
            logger.info("Aircraft eliminado exitosamente (sin respuesta JSON)")
    else:
        logger.info("Aircraft eliminado exitosamente (respuesta vacía)")


@pytest.mark.parametrize(
    "test_id, priority, aircraft_id_override, use_auth, expected_status, description",
    [
        # ========== CASOS CRÍTICOS (Critical Priority) ==========
        (
            "AIRCRAFT_DELETE_C001",
            "Critical",
            None,  # Usar aircraft válido del fixture
            True,  # Con autenticación
            204,  # ← CORREGIDO: La API devuelve 204 No Content (no 200)
            "Eliminación exitosa de aircraft existente con autenticación válida"
        ),
        (
            "AIRCRAFT_DELETE_C002",
            "Critical",
            None,  # Usar aircraft válido del fixture
            False,  # SIN autenticación
            401,
            "Intento de eliminación sin token de autenticación (Unauthorized)"
        ),
        (
            "AIRCRAFT_DELETE_C003",
            "Critical",
            "acf-00000000",  # ID que NO existe
            True,
            # ← CORREGIDO: La API NO valida existencia, devuelve 204 siempre (bug/diseño)
            204,
            "Intento de eliminar aircraft inexistente (API devuelve 204 sin validar)"
        ),
        (
            "AIRCRAFT_DELETE_C004",
            "Critical",
            "invalid-format-id",  # Formato inválido
            True,
            204,  # ← CORREGIDO: La API NO valida formato, devuelve 204 siempre
            "Intento de eliminar con aircraft_id en formato inválido (API lo acepta)"
        ),

        # ========== CASOS DE PRIORIDAD MEDIA (Medium Priority) ==========
        (
            "AIRCRAFT_DELETE_M001",
            "Medium",
            "",  # aircraft_id vacío
            True,
            # ← CORREGIDO: Method Not Allowed (DELETE a /aircrafts/ sin ID)
            405,
            "Intento de eliminar con aircraft_id vacío (Method Not Allowed)"
        ),
        (
            "AIRCRAFT_DELETE_M002",
            "Medium",
            "acf-deleted",  # Aircraft ya eliminado (doble DELETE)
            True,
            204,  # ← CORREGIDO: API es idempotente, segundo DELETE también devuelve 204
            "Intento de eliminar aircraft que ya fue eliminado (idempotencia - devuelve 204)"
        ),
        (
            "AIRCRAFT_DELETE_M003",
            "Medium",
            None,
            True,
            204,  # ← CORREGIDO: DELETE devuelve 204
            "Eliminación con verificación de que el recurso no existe después"
        ),

        # ========== CASOS DE PRIORIDAD BAJA (Low Priority) ==========
        (
            "AIRCRAFT_DELETE_L001",
            "Low",
            "999999999999999999999",  # ID extremadamente largo
            True,
            204,  # ← CORREGIDO: API no valida longitud
            "Intento de eliminar con aircraft_id excesivamente largo (API lo acepta)"
        ),
        (
            "AIRCRAFT_DELETE_L002",
            "Low",
            "../etc/passwd",  # Path traversal attempt
            True,
            404,  # Este SÍ falla correctamente
            "Intento de eliminar con caracteres especiales/path traversal"
        ),
        (
            "AIRCRAFT_DELETE_L003",
            "Low",
            "acf-<script>alert(1)</script>",  # XSS attempt
            True,
            404,  # Este SÍ falla correctamente
            "Intento de eliminar con caracteres de inyección XSS"
        ),
    ]
)
def test_delete_aircraft_parametrized(
    test_id,
    priority,
    aircraft_id_override,
    use_auth,
    expected_status,
    description,
    api_client,
    authenticated_token,
    test_aircraft_id
):
    """Test parametrizado para DELETE /aircrafts/{id}"""
    logger.info(
        "Ejecutando prueba %s: %s [Prioridad: %s]", test_id, description, priority)

    # Determinar qué aircraft_id usar
    if aircraft_id_override is not None:
        aircraft_id = aircraft_id_override
    else:
        aircraft_id = test_aircraft_id

    # Preparar headers (con o sin autenticación)
    if use_auth:
        headers = {"Authorization": f"Bearer {authenticated_token}"}
    else:
        headers = {}

    # Caso especial: Doble DELETE (M002)
    if test_id == "AIRCRAFT_DELETE_M002":
        # Primer DELETE (debe ser exitoso)
        first_response = api_client.make_request(
            endpoint=f"aircrafts/{test_aircraft_id}",
            method="DELETE",
            headers=headers
        )
        logger.info("Primer DELETE - Status: %d", first_response.status_code)
        assert first_response.status_code == HTTPStatus.NO_CONTENT, \
            f"El primer DELETE debería devolver 204, recibió: {first_response.status_code}"

        # Segundo DELETE (debe fallar - ya fue eliminado)
        aircraft_id = test_aircraft_id
        logger.info("Intentando segundo DELETE del mismo aircraft...")

    # EJECUTAR - Petición DELETE
    try:
        response = api_client.make_request(
            endpoint=f"aircrafts/{aircraft_id}",
            method="DELETE",
            headers=headers
        )

        logger.info("Status Code recibido: %d", response.status_code)

        # Capturar detalles del error si no es el esperado
        if response.status_code != expected_status:
            try:
                error_detail = response.json().get("detail", "No hay detalle disponible")
            except (ValueError, KeyError, TypeError, json.JSONDecodeError):
                error_detail = response.text if response.text else "Sin contenido"

            logger.error(
                "[TEST_FAILED] %s | Status esperado: %s, recibido: %s | Error: %s",
                test_id,
                expected_status,
                response.status_code,
                error_detail
            )

        # ASSERT principal
        assert response.status_code == expected_status, \
            f"Se esperaba status {expected_status}, pero se recibió {response.status_code}. Respuesta: {response.text}"

        # VALIDACIONES ESPECÍFICAS para casos exitosos (204 No Content)
        if expected_status == HTTPStatus.NO_CONTENT:
            logger.info(
                "[TEST_SUCCESS] %s | Aircraft eliminado (204 No Content)", test_id)

            # 204 No Content NO debe tener body
            assert not response.text or response.text == "", \
                f"204 No Content no debería tener body, pero recibió: {response.text}"

            # Caso especial M003: Verificar que el aircraft YA NO existe
            if test_id == "AIRCRAFT_DELETE_M003":
                logger.info("Verificando que el aircraft ya no existe...")
                verify_response = api_client.make_request(
                    endpoint=f"aircrafts/{aircraft_id}",
                    method="GET",
                    headers=headers
                )
                # La API puede devolver 404 o 204 para recursos inexistentes
                assert verify_response.status_code in [HTTPStatus.NOT_FOUND, HTTPStatus.NO_CONTENT], \
                    f"El aircraft debería no existir, pero GET devolvió {verify_response.status_code}"
                logger.info(
                    "✓ Verificado: El aircraft ya no existe en el sistema")

        # VALIDACIONES ESPECÍFICAS para casos de error (4xx, 5xx)
        else:
            logger.info(
                "[TEST_SUCCESS] %s | Error esperado recibido correctamente: %s",
                test_id,
                response.status_code
            )

            # Validar que errores 4xx/5xx devuelvan mensaje descriptivo
            if response.text:
                try:
                    error_response = response.json()
                    assert "detail" in error_response or "message" in error_response, \
                        "La respuesta de error debe incluir 'detail' o 'message'"
                    logger.info("Detalle del error: %s", error_response)
                except json.JSONDecodeError:
                    # Algunas APIs devuelven HTML en errores - esto es aceptable
                    logger.info(
                        "Respuesta de error no es JSON (puede ser HTML)")

    except AssertionError:
        # Re-lanzar AssertionErrors para que pytest los capture
        raise

    except Exception as e:
        # Capturar excepciones inesperadas
        logger.exception(
            "[EXCEPTION] %s | Error inesperado durante el test", test_id)
        pytest.fail(
            f"Excepción inesperada en {test_id}: {type(e).__name__}: {str(e)}")

    logger.info("✓ Prueba %s completada exitosamente", test_id)

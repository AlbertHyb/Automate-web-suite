import pytest
import json
import time
import requests
import logging
import traceback
# Importamos el fixture desde conftest.py
from api.tests.conftest import logger, airport_test_data


# Configurar el logger para que no propague mensajes a la consola
logger = logging.getLogger(__name__)


class AirportsPage:
    def __init__(self, api_client):
        self.api_client = api_client
        self.endpoint = "airports"  # No dejar la URL completa ni visible

    def get_airport(self, iata_code, headers=None):
        endpoint = f"{self.endpoint}/{iata_code}"
        # Usamos None como data porque es una petición GET y no necesita cuerpo
        return self.api_client.make_request(
            method="GET",
            endpoint=endpoint,
            data=None,  # GET no necesita datos en el cuerpo
            headers=headers or {}
        )


def fetch_airport_by_iata(iata_code, api_client):
    airport_page = AirportsPage(api_client)
    # Headers básicos - pueden ser necesarios según la API
    headers = {"Accept": "application/json"}

    start_time = time.time()

    try:
        # Llamar al método GET de AirportsPage
        response = airport_page.get_airport(iata_code, headers=headers)

        duration = time.time() - start_time

        # Registrar la respuesta en el log con información detallada
        if response.status_code == 200:
            data = response.json()
            logger.info(
                f"[IATA_SUCCESS] Código={iata_code} | Status={response.status_code} | "
                f"Duración={duration:.3f}s | "
                f"Ciudad={data.get('city', 'N/A')} | País={data.get('country', 'N/A')} | "
                f"Datos completos: {json.dumps(data, indent=2, ensure_ascii=False)}"
            )
        else:
            try:
                error_data = response.json()
                error_detail = error_data.get('detail', 'No detail provided')
                logger.error(
                    f"[IATA_ERROR] Código={iata_code} | Status={response.status_code} | "
                    f"Duración={duration:.3f}s | "
                    f"Error={error_detail} | "
                    f"Headers enviados={headers} | "
                    f"Respuesta completa: {json.dumps(error_data, indent=2, ensure_ascii=False)}"
                )
            except:
                logger.error(
                    f"[IATA_ERROR] Código={iata_code} | Status={response.status_code} | "
                    f"Duración={duration:.3f}s | "
                    f"Headers enviados={headers} | "
                    f"Respuesta no JSON: {response.text}"
                )

        return response
    except Exception as e:
        duration = time.time() - start_time
        error_type = type(e).__name__
        logger.error(
            f"[IATA_EXCEPTION] Código={iata_code} | Tipo={error_type} | "
            f"Duración={duration:.3f}s | "
            f"Headers enviados={headers} | "
            f"Mensaje de error: {str(e)} | "
            f"Traza: {traceback.format_exc()}"
        )
        # Crear una respuesta fallida similar a requests para mantener consistencia
        fake_response = requests.Response()
        fake_response.status_code = 500
        fake_response._content = json.dumps({
            "detail": str(e),
            "error_type": error_type,
            "endpoint": f"airports/{iata_code}"
        }).encode('utf-8')
        return fake_response


# Pruebas parametrizadas para el endpoint de aeropuertos por código IATA
@pytest.mark.parametrize("test_case", [
    {
        "id": "valid_iata_code",
        "description": "Código IATA válido devuelve 200 y datos correctos",
        "use_valid_iata": True,
        "expected_status": 200,
        "verify_fields": True
    },
    {
        "id": "invalid_iata_code",
        "description": "Código IATA inexistente devuelve 404",
        "use_valid_iata": False,
        "expected_status": 404,
        "verify_fields": False
    }
])
def test_iata_endpoint_parametrized(test_case, airport_test_data, api_client):
    # Seleccionar el código IATA según el caso de prueba
    iata_code = airport_test_data["valid_iata"] if test_case["use_valid_iata"] else airport_test_data["invalid_iata"]

    # Registrar información detallada del inicio de la prueba
    logger.info(
        f"[TEST_START] ID={test_case['id']} | "
        f"Descripción={test_case['description']} | "
        f"IATA={iata_code} | "
        f"Status esperado={test_case['expected_status']}"
    )

    start_time = time.time()

    # Realizar la solicitud
    response = fetch_airport_by_iata(iata_code, api_client)

    duration = time.time() - start_time

    # Verificar el código de estado
    status_match = response.status_code == test_case["expected_status"]

    if not status_match:
        logger.error(
            f"[TEST_FAIL] ID={test_case['id']} | "
            f"IATA={iata_code} | "
            f"Status esperado={test_case['expected_status']} | "
            f"Status recibido={response.status_code} | "
            f"Duración={duration:.3f}s"
        )

    assert status_match, \
        f"Se esperaba status code {test_case['expected_status']} para {iata_code}, pero se recibió {response.status_code}"

    # Si es un caso exitoso, verificar la estructura de la respuesta
    if test_case["expected_status"] == 200 and test_case["verify_fields"]:
        data = response.json()

        # Verificar campos requeridos
        fields_ok = True
        missing_fields = []

        if "iata_code" not in data:
            fields_ok = False
            missing_fields.append("iata_code")

        if "city" not in data:
            fields_ok = False
            missing_fields.append("city")

        if "country" not in data:
            fields_ok = False
            missing_fields.append("country")

        if not fields_ok:
            logger.error(
                f"[TEST_FAIL_FIELDS] ID={test_case['id']} | "
                f"IATA={iata_code} | "
                f"Campos faltantes={missing_fields} | "
                f"Datos recibidos={json.dumps(data, indent=2, ensure_ascii=False)}"
            )

        assert "iata_code" in data, f"El campo 'iata_code' no está presente en la respuesta para {iata_code}"
        assert "city" in data, f"El campo 'city' no está presente en la respuesta para {iata_code}"
        assert "country" in data, f"El campo 'country' no está presente en la respuesta para {iata_code}"

        # Verificar que el código IATA en la respuesta coincida con el solicitado
        iata_match = data["iata_code"] == iata_code

        if not iata_match:
            logger.error(
                f"[TEST_FAIL_IATA_MISMATCH] ID={test_case['id']} | "
                f"IATA solicitado={iata_code} | "
                f"IATA recibido={data['iata_code']} | "
                f"Datos recibidos={json.dumps(data, indent=2, ensure_ascii=False)}"
            )

        assert iata_match, \
            f"El código IATA en la respuesta ({data['iata_code']}) no coincide con el solicitado ({iata_code})"

        # Actualizar el mensaje de éxito para incluir los datos completos
        logger.info(
            f"[TEST_SUCCESS] ID={test_case['id']} | "
            f"IATA={iata_code} | "
            f"Status={response.status_code} | "
            f"Duración={duration:.3f}s | "
            f"Ciudad={data.get('city', 'N/A')} | "
            f"País={data.get('country', 'N/A')} | "
            f"Datos completos: {json.dumps(data, indent=2, ensure_ascii=False)}"
        )
    else:
        # Para casos de error, registrar también la respuesta completa
        try:
            error_data = response.json()
            logger.info(
                f"[TEST_SUCCESS] ID={test_case['id']} | "
                f"IATA={iata_code} | "
                f"Status={response.status_code} | "
                f"Duración={duration:.3f}s | "
                f"Respuesta completa: {json.dumps(error_data, indent=2, ensure_ascii=False)}"
            )
        except:
            logger.info(
                f"[TEST_SUCCESS] ID={test_case['id']} | "
                f"IATA={iata_code} | "
                f"Status={response.status_code} | "
                f"Duración={duration:.3f}s | "
                f"Respuesta: {response.text}"
            )

# Se puede agregar más casos de prueba extendiendo la parametrización


@pytest.mark.parametrize("iata_index", [0, 1, 2])
def test_multiple_valid_iata_codes(iata_index, airport_test_data, api_client):
    # Asegurarse de que hay suficientes aeropuertos para la prueba
    if len(airport_test_data["airports"]) <= iata_index:
        reason = f"No hay suficientes aeropuertos para probar el índice {iata_index}"
        logger.warning(
            f"[TEST_SKIP] Razón: {reason} | Total aeropuertos disponibles: {len(airport_test_data['airports'])}")
        pytest.skip(reason)

    # Obtener el código IATA según el índice
    valid_iata = airport_test_data["airports"][iata_index]["iata_code"]

    logger.info(
        f"[TEST_START_MULTI] Índice={iata_index} | "
        f"IATA={valid_iata} | "
        f"Total aeropuertos={len(airport_test_data['airports'])}"
    )

    start_time = time.time()

    # Realizar la solicitud
    response = fetch_airport_by_iata(valid_iata, api_client)

    duration = time.time() - start_time

    # Verificar el código de estado
    status_ok = response.status_code == 200

    if not status_ok:
        logger.error(
            f"[TEST_FAIL_MULTI] Índice={iata_index} | "
            f"IATA={valid_iata} | "
            f"Status esperado=200 | "
            f"Status recibido={response.status_code} | "
            f"Duración={duration:.3f}s"
        )

    assert status_ok, \
        f"Se esperaba status code 200 para código válido {valid_iata}, pero se recibió {response.status_code}"

    # Verificar la estructura y coherencia de la respuesta
    data = response.json()

    if "iata_code" not in data:
        logger.error(
            f"[TEST_FAIL_MULTI_FIELDS] Índice={iata_index} | "
            f"IATA={valid_iata} | "
            f"Campo faltante=iata_code | "
            f"Datos recibidos={json.dumps(data, indent=2, ensure_ascii=False)}"
        )

    assert "iata_code" in data, f"El campo 'iata_code' no está presente en la respuesta para {valid_iata}"

    iata_match = data["iata_code"] == valid_iata

    if not iata_match:
        logger.error(
            f"[TEST_FAIL_MULTI_IATA_MISMATCH] Índice={iata_index} | "
            f"IATA solicitado={valid_iata} | "
            f"IATA recibido={data['iata_code']} | "
            f"Datos recibidos={json.dumps(data, indent=2, ensure_ascii=False)}"
        )

    assert iata_match, \
        f"El código IATA en la respuesta ({data['iata_code']}) no coincide con el solicitado ({valid_iata})"

    # Actualizar el mensaje de éxito para incluir los datos completos
    logger.info(
        f"[TEST_SUCCESS_MULTI] Índice={iata_index+1} | "
        f"IATA={valid_iata} | "
        f"Status={response.status_code} | "
        f"Duración={duration:.3f}s | "
        f"Ciudad={data.get('city', 'N/A')} | "
        f"País={data.get('country', 'N/A')} | "
        f"Datos completos: {json.dumps(data, indent=2, ensure_ascii=False)}"
    )

import pytest
import json
import time
import requests
import logging
import traceback

logger = logging.getLogger(__name__)

class AirportsPage:
    def __init__(self, api_client):
        self.api_client = api_client
        self.endpoint = "airports"  # No dejar la URL completa ni visible

    def put_airport(self, iata_code, headers):
        endpoint = f"{self.endpoint}/{iata_code}"

        data = {
            "iata_code": iata_code,
            "city": "string",
            "country": "string"
        }

        return self.api_client.make_request(
            method="PUT",
            endpoint=endpoint,
            data=data,
            headers=headers or {}
        )


def update_airport_by_iata(iata_code, api_client,payload):
    airport_page = AirportsPage(api_client)
    # Headers básicos - pueden ser necesarios según la API
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    start_time = time.time()
    logger.debug(f"Enviando solicitud PUT para IATA={iata_code} con payload={json.dumps(payload, ensure_ascii=False)}")

    try:
        response = airport_page.put_airport(iata_code, payload=payload, headers=headers)

        duration = time.time() - start_time

        # Registrar la respuesta en el log con información detallada
        if response.status_code == 201:
            data = response.json()
            logger.info(
                f"[IATA_UPDATE_SUCCESS] Código={iata_code} | Status={response.status_code} | "
                f"Duración={duration:.3f}s | "
                f"Ciudad={data.get('city', 'N/A')} | País={data.get('country', 'N/A')} | "
                f"Datos completos: {json.dumps(data, indent=2, ensure_ascii=False)}"
            )
        else:
            try:
                error_data = response.json()
                error_detail = error_data.get('detail', 'No detail provided')
                logger.error(
                    f"[IATA_UPDATE_ERROR] Código={iata_code} | Status={response.status_code} | "
                    f"Duración={duration:.3f}s | "
                    f"Error={error_detail} | "
                    f"Headers enviados={headers} | Payload={json.dumps(payload, ensure_ascii=False)} | "
                    f"Respuesta completa: {json.dumps(error_data, indent=2, ensure_ascii=False)}"
                )
            except:
                logger.error(
                    f"[IATA_UPDATE_ERROR] Código={iata_code} | Status={response.status_code} | "
                    f"Duración={duration:.3f}s | "
                    f"Headers enviados={headers} | Payload={json.dumps(payload, ensure_ascii=False)} | "
                    f"Respuesta no JSON: {response.text}"
                )

        return response
    except Exception as e:
        duration = time.time() - start_time
        error_type = type(e).__name__
        logger.error(
            f"[IATA_UPDATE_EXCEPTION] Código={iata_code} | Tipo={error_type} | "
            f"Duración={duration:.3f}s | "
            f"Headers enviados={headers} | Payload={json.dumps(payload, ensure_ascii=False)} | "
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


@pytest.mark.parametrize(
    "iata_code, payload, expected_status, importance",
    [
        # Casos críticos
        pytest.param("ABC", {"iata_code": "ABC", "city": "Nueva Ciudad", "country": "España"}, 200, "CRÍTICO",
                     id="critico-actualizar-ciudad-pais"),
        pytest.param("XYZ", {"iata_code": "XYZ", "city": "Ciudad Test", "country": "México"}, 200, "CRÍTICO",
                     id="critico-ciudad-pais-alternativo"),
        pytest.param("TYB", None, 400, "CRÍTICO",
                     id="critico-payload-nulo"),
        pytest.param("ABC", {"iata_code": "DEF", "city": "Ciudad", "country": "País"}, 400, "CRÍTICO",
                     id="critico-iata-incorrecto"),

        # Caso de importancia media
        pytest.param("123", {"iata_code": "123", "city": "Ciudad Media", "country": "Colombia"}, 200, "MEDIO",
                     id="medio-actualizar-normal"),

        # Caso de importancia baja
        pytest.param("DEF", {"iata_code": "DEF", "city": "", "country": ""}, 200, "BAJO",
                     id="bajo-campos-vacios")
    ]
)
def test_update_airport(iata_code, payload, expected_status, importance, api_client):

    logger.info(
        f"[TEST_START_UPDATE] IATA={iata_code} | "
        f"Expected Status={expected_status} | "
        f"Importancia={importance} | "
        f"Payload={json.dumps(payload, ensure_ascii=False) if payload else 'None'}"
    )

    start_time = time.time()

    # Realizar la solicitud
    response = update_airport_by_iata(iata_code, api_client, payload)

    duration = time.time() - start_time

    # Verificar el código de estado
    status_ok = response.status_code == expected_status

    if not status_ok:
        logger.error(
            f"[TEST_FAIL_UPDATE] IATA={iata_code} | "
            f"Status esperado={expected_status} | "
            f"Status recibido={response.status_code} | "
            f"Importancia={importance} | "
            f"Duración={duration:.3f}s | "
            f"Payload={json.dumps(payload, ensure_ascii=False) if payload else 'None'}"
        )

    assert status_ok, \
        f"Se esperaba status code {expected_status} para IATA {iata_code}, pero se recibió {response.status_code}"

    # Solo verificar datos de la respuesta si el estado esperado es 200
    if expected_status == 200:
        data = response.json()

        # Verificar la presencia del campo iata_code
        if "iata_code" not in data:
            logger.error(
                f"[TEST_FAIL_UPDATE_FIELDS] IATA={iata_code} | "
                f"Campo faltante=iata_code | "
                f"Importancia={importance} | "
                f"Datos recibidos={json.dumps(data, indent=2, ensure_ascii=False)}"
            )
        assert "iata_code" in data, f"El campo 'iata_code' no está presente en la respuesta para {iata_code}"

        # Verificar que el iata_code en la respuesta coincide con el solicitado
        iata_match = data["iata_code"] == iata_code
        if not iata_match:
            logger.error(
                f"[TEST_FAIL_UPDATE_IATA_MISMATCH] IATA solicitado={iata_code} | "
                f"IATA recibido={data['iata_code']} | "
                f"Importancia={importance} | "
                f"Datos recibidos={json.dumps(data, indent=2, ensure_ascii=False)}"
            )
        assert iata_match, \
            f"El código IATA en la respuesta ({data['iata_code']}) no coincide con el solicitado ({iata_code})"

        # Verificar que los datos actualizados coinciden con el payload
        if payload:
            for key in ["city", "country"]:
                if key in payload:
                    value_match = data.get(key) == payload[key]
                    if not value_match:
                        logger.error(
                            f"[TEST_FAIL_UPDATE_FIELD_MISMATCH] IATA={iata_code} | "
                            f"Campo={key} | "
                            f"Valor esperado={payload[key]} | "
                            f"Valor recibido={data.get(key, 'N/A')} | "
                            f"Importancia={importance} | "
                            f"Datos recibidos={json.dumps(data, indent=2, ensure_ascii=False)}"
                        )
                    assert value_match, \
                        f"El campo '{key}' en la respuesta ({data.get(key, 'N/A')}) no coincide con el enviado ({payload[key]})"

        # Registrar éxito de la prueba
    logger.info(
        f"[TEST_SUCCESS_UPDATE] IATA={iata_code} | "
        f"Status={response.status_code} | "
        f"Importancia={importance} | "
        f"Duración={duration:.3f}s | "
        f"Payload={json.dumps(payload, ensure_ascii=False) if payload else 'None'} | "
        f"Datos recibidos={json.dumps(response.json(), indent=2, ensure_ascii=False) if response.status_code == 200 else response.text}"
    )
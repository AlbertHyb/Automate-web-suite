import pytest
import json
import time
import requests
import logging
import traceback
from api.tests.conftest import logger, airport_test_data
from api.tests.airports.list_airports import fetch_data


# Configurar el logger para que no propague mensajes a la consola
logger = logging.getLogger(__name__)

class AirportsPage:
    def __init__(self, api_client):
        self.api_client = api_client
        self.endpoint = "airports"  # No dejar la URL completa ni visible

    def delete_airport(self, iata_code, headers=None):
        endpoint = f"{self.endpoint}/{iata_code}"
        # Usamos None como data porque es una petición DELETE y no necesita cuerpo
        return self.api_client.make_request(
            method="DELETE",
            endpoint=endpoint,
            data=None,
            headers=headers or {}
        )

    def create_airport(self, airport_data, headers=None):
        endpoint = f"{self.endpoint}"
        return self.api_client.make_request(
            method="POST",
            endpoint=endpoint,
            data=airport_data,
            headers=headers or {}
        )


def create_airport_by_iata(airport_data, api_client):
    airport_page = AirportsPage(api_client)
    # Headers básicos - pueden ser necesarios según la API
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    start_time = time.time()
    iata_code = airport_data.get("iata_code", "UNKNOWN")
    logger.debug(f"Enviando solicitud POST para crear aeropuerto con IATA={iata_code}")

    try:
        response = airport_page.create_airport(airport_data, headers=headers)

        duration = time.time() - start_time

        # Registrar la respuesta en el log con información detallada
        if response.status_code == 201:
            logger.info(
                f"[IATA_POST_SUCCESS] Código={iata_code} | Status={response.status_code} | "
                f"Duración={duration:.3f}s"
            )
        else:
            try:
                error_data = response.json()
                error_detail = error_data.get('detail', 'No detail provided')
                logger.error(
                    f"[IATA_POST_ERROR] Código={iata_code} | Status={response.status_code} | "
                    f"Duración={duration:.3f}s | "
                    f"Error={error_detail} | "
                    f"Headers enviados={headers} | "
                    f"Datos enviados={json.dumps(airport_data, indent=2, ensure_ascii=False)} | "
                    f"Respuesta completa: {json.dumps(error_data, indent=2, ensure_ascii=False)}"
                )
            except:
                logger.error(
                    f"[IATA_POST_ERROR] Código={iata_code} | Status={response.status_code} | "
                    f"Duración={duration:.3f}s | "
                    f"Headers enviados={headers} | "
                    f"Datos enviados={json.dumps(airport_data, indent=2, ensure_ascii=False)} | "
                    f"Respuesta no JSON: {response.text}"
                )
        return response
    except Exception as e:
        duration = time.time() - start_time
        error_type = type(e).__name__
        logger.error(
            f"[IATA_POST_EXCEPTION] Código={iata_code} | Tipo={error_type} | "
            f"Duración={duration:.3f}s | "
            f"Headers enviados={headers} | "
            f"Datos enviados={json.dumps(airport_data, indent=2, ensure_ascii=False)} | "
            f"Mensaje de error: {str(e)} | "
            f"Traza: {traceback.format_exc()}"
        )

        # Crear una respuesta fallida similar a requests para mantener consistencia
        fake_response = requests.Response()
        fake_response.status_code = 500
        fake_response._content = json.dumps({
            "detail": str(e),
            "error_type": error_type,
            "endpoint": "airports"
        }).encode('utf-8')
        return fake_response


def delete_airport_by_iata(iata_code, api_client):
    airport_page = AirportsPage(api_client)
    # Headers básicos - pueden ser necesarios según la API
    headers = {"Accept": "application/json"}

    start_time = time.time()
    logger.debug(f"Enviando solicitud DELETE para IATA={iata_code}")

    try:
        response = airport_page.delete_airport(iata_code, headers=headers)

        duration = time.time() - start_time

        # Registrar la respuesta en el log con información detallada
        if response.status_code == 200:
            logger.info(
                f"[IATA_DELETE_SUCCESS] Código={iata_code} | Status={response.status_code} | "
                f"Duración={duration:.3f}s"
            )

        else:
           try:
               error_data = response.json()
               error_detail = error_data.get('detail', 'No detail provided')
               logger.error(
                   f"[IATA_DELETE_ERROR] Código={iata_code} | Status={response.status_code} | "
                   f"Duración={duration:.3f}s | "
                   f"Error={error_detail} | "
                   f"Headers enviados={headers} | "
                   f"Respuesta completa: {json.dumps(error_data, indent=2, ensure_ascii=False)}"
        )
           except:
              logger.error(
                 f"[IATA_DELETE_ERROR] Código={iata_code} | Status={response.status_code} | "
                 f"Duración={duration:.3f}s | "
                 f"Headers enviados={headers} | "
                 f"Respuesta no JSON: {response.text}"
              )
        return response
    except Exception as e:
        duration = time.time() - start_time
        error_type = type(e).__name__
        logger.error(
            f"[IATA_DELETE_EXCEPTION] Código={iata_code} | Tipo={error_type} | "
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


@pytest.mark.parametrize(
    "test_id, priority, iata_code, expected_status, description",
    [
        # Casos críticos
        (
                "DELETE_C001",
                "Critical",
                None,  # None porque obtendremos un código IATA de la lista
                200,
                "Eliminar aeropuerto existente con IATA válido"
        ),
        (
                "DELETE_C002",
                "Critical",
                "XYZ",
                404,
                "Eliminar aeropuerto con IATA inexistente"
        ),
        (
                "DELETE_C003",
                "Critical",
                "",
                200,
                "Eliminar aeropuerto sin proporcionar código IATA"
        ),

        # Caso de importancia media
        (
                "DELETE_M001",
                "Medium",
                "TY1",
                404,
                "Eliminar aeropuerto con IATA que contiene caracteres no alfabéticos"
        ),

        # Caso de importancia baja
        (
                "DELETE_L001",
                "Low",
                "TYBB",
                404,
                "Eliminar aeropuerto con IATA que excede longitud máxima (3 caracteres)"
        ),
    ]
)
def test_delete_airport(test_id, priority, iata_code, expected_status, description, api_client):
    logger.info(f"Ejecutando prueba {test_id}: {description} [Prioridad: {priority}]")

    # Para el caso exitoso, obtenemos un aeropuerto existente de la lista
    if test_id == "DELETE_C001":
        try:
            # Obtener lista de aeropuertos existentes
            response = fetch_data(skip=0, limit=5, api_client=api_client)

            if response.status_code == 200 and len(response.json()) > 0:
                # Seleccionar el primer aeropuerto de la lista
                airport = response.json()[0]
                iata_code = airport.get("iata_code")
                logger.info(f"Usando aeropuerto existente con IATA={iata_code}")
            else:
                # Si no hay aeropuertos existentes, crear uno nuevo
                logger.warning("No se encontraron aeropuertos existentes, creando uno nuevo...")
                airport_data = {"iata_code": "TYB", "city": "Test City", "country": "Test Country"}
                create_response = create_airport_by_iata(airport_data, api_client)
                if create_response.status_code == 201:
                    iata_code = "TYB"
                else:
                    logger.error(f"No se pudo crear aeropuerto: {create_response.text}")
                    pytest.skip("No se pudo preparar la prueba: no hay aeropuertos disponibles")
        except Exception as e:
            logger.warning(f"Error al obtener aeropuertos existentes: {str(e)}")
            # Como fallback, intentamos con el código predefinido
            iata_code = "TYB"
            airport_data = {"iata_code": iata_code, "city": "Test City", "country": "Test Country"}
            create_airport_by_iata(airport_data, api_client)

    # Ejecutar la prueba
    response = delete_airport_by_iata(iata_code, api_client)

    # Verificar resultado
    assert response.status_code == expected_status, \
        f"Se esperaba status {expected_status}, pero se recibió {response.status_code}. Respuesta: {response.text}"

    logger.info(f"Prueba {test_id} completada con éxito")

import logging
import time
import traceback
import json
import requests
from api.pages.aircraft_page import AircraftPage

logger = logging.getLogger(__name__)

def update_aircraft_request(aircraft_id, aircraft_data, api_client, auth_headers=None):
    """Helper para actualizar aviones usando PUT."""
    aircraft_page = AircraftPage(api_client)

    # Preparar headers con autenticación
    headers = {"Content-Type": "application/json"}
    if auth_headers:
        headers.update(auth_headers)

    start_time = time.time()
    model = aircraft_data.get("model", "UNKNOWN")
    logger.debug(f"Enviando solicitud PUT para actualizar avión id={aircraft_id}, modelo={model}")

    try:
        # Llamar al método update_aircraft
        response = aircraft_page.update_aircraft(
            aircraft_id=aircraft_id,
            aircraft_data=aircraft_data,
            headers=headers
        )

        duration = time.time() - start_time

        # Logging según el resultado
        if response.status_code == 200:
            logger.info(
                f"[AIRCRAFT_PUT_SUCCESS] ID={aircraft_id} | Modelo={model} | Status={response.status_code} | "
                f"Duración={duration:.3f}s"
            )
        else:
            try:
                error_data = response.json()
                error_detail = error_data.get('detail', 'No detail provided')
                logger.error(
                    f"[AIRCRAFT_PUT_ERROR] ID={aircraft_id} | Modelo={model} | Status={response.status_code} | "
                    f"Duración={duration:.3f}s | "
                    f"Error={error_detail} | "
                    f"Headers enviados={headers} | "
                    f"Datos enviados={json.dumps(aircraft_data, indent=2, ensure_ascii=False)} | "
                    f"Respuesta completa: {json.dumps(error_data, indent=2, ensure_ascii=False)}"
                )
            except:
                logger.error(
                    f"[AIRCRAFT_PUT_ERROR] ID={aircraft_id} | Modelo={model} | Status={response.status_code} | "
                    f"Duración={duration:.3f}s | "
                    f"Headers enviados={headers} | "
                    f"Datos enviados={json.dumps(aircraft_data, indent=2, ensure_ascii=False)} | "
                    f"Respuesta no JSON: {response.text}"
                )
        return response

    except Exception as e:
        duration = time.time() - start_time
        error_type = type(e).__name__
        logger.error(
            f"[AIRCRAFT_PUT_EXCEPTION] ID={aircraft_id} | Modelo={model} | Tipo={error_type} | "
            f"Duración={duration:.3f}s | "
            f"Headers enviados={headers} | "
            f"Datos enviados={json.dumps(aircraft_data, indent=2, ensure_ascii=False)} | "
            f"Mensaje de error: {str(e)} | "
            f"Traza: {traceback.format_exc()}"
        )
        raise
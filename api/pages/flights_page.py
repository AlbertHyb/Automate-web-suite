import time
import json
import logging
import traceback
from typing import Dict, Any, Optional
from jsonschema import validate
from api.schemas.search_schema import flight_search_schema

logger = logging.getLogger(__name__)

class FlightsAPI:
    """Cliente reutilizable para operaciones de vuelos (crear y buscar)."""
    def __init__(self, api_client):
        self.api_client = api_client
        self.endpoint = "flights"

    def create_flight(self, flight_data: Dict[str, Any], headers: Optional[Dict[str, str]] = None):
        start_time = time.time()
        try:
            response = self.api_client.make_request(
                method="POST",
                endpoint=self.endpoint,
                data=flight_data,
                headers=headers or {"Content-Type": "application/json", "Accept": "application/json"}
            )
            duration = time.time() - start_time
            if response.status_code == 201:
                logger.info(f"[FLIGHTS_POST_SUCCESS] Status={response.status_code} Duración={duration:.3f}s")
            else:
                self._log_error("FLIGHTS_POST_ERROR", response, flight_data, headers, duration)
            return response
        except Exception as e:
            duration = time.time() - start_time
            self._log_exception("FLIGHT_POST_EXCEPTION", e, flight_data, headers, duration)
            raise

    def search_flight(self, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        # Validación opcional de esquema (solo parámetros relevantes)
        if params:
            try:
                validate(instance=params, schema=flight_search_schema)
            except Exception as schema_err:
                logger.warning(f"[FLIGHTS_SCHEMA_WARNING] Params no cumplen schema: {schema_err} | Params={params}")
        start_time = time.time()
        try:
            response = self.api_client.make_request(
                method="GET",
                endpoint=self.endpoint,
                data=params,
                headers=headers or {"Accept": "application/json"}
            )
            duration = time.time() - start_time
            if response.status_code == 200:
                logger.info(f"[FLIGHTS_GET_SUCCESS] Status={response.status_code} Duración={duration:.3f}s Params={params}")
            else:
                self._log_error("FLIGHTS_GET_ERROR", response, params, headers, duration)
            return response
        except Exception as e:
            duration = time.time() - start_time
            self._log_exception("FLIGHT_GET_EXCEPTION", e, params, headers, duration)
            raise

    def _log_error(self, tag: str, response, data, headers, duration: float):
        try:
            body = response.json()
        except Exception:
            body = response.text
        logger.error(
            f"[{tag}] Status={response.status_code} Duración={duration:.3f}s Data={json.dumps(data, ensure_ascii=False)} "
            f"Headers={headers} Body={body}"
        )

    def _log_exception(self, tag: str, exc: Exception, data, headers, duration: float):
        logger.error(
            f"[{tag}] Duración={duration:.3f}s Data={data} Headers={headers} Error={exc} Traza={traceback.format_exc()}"
        )

# Funciones helper conservando nombres similares a los usados en tests existentes

def create_flight_request(flight_data, api_client, auth_headers=None):
    flights_api = FlightsAPI(api_client)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if auth_headers:
        headers.update(auth_headers)
    return flights_api.create_flight(flight_data, headers=headers)

def search_flight_request(search_params, api_client, auth_headers=None):
    flights_api = FlightsAPI(api_client)
    headers = {"Accept": "application/json"}
    if auth_headers:
        headers.update(auth_headers)
    return flights_api.search_flight(params=search_params, headers=headers)


import pytest
import logging
import time
import json
from http import HTTPStatus
from datetime import datetime, timedelta



logger = logging.getLogger(__name__)


def generate_flight_times(hours_from_now=2, flight_duration=5):
    """Genera tiempos de salida y llegada válidos para un vuelo."""
    now = datetime.utcnow()
    departure = now + timedelta(hours=hours_from_now)
    arrival = departure + timedelta(hours=flight_duration)
    return departure.strftime("%Y-%m-%dT%H:%M:%S"), arrival.strftime("%Y-%m-%dT%H:%M:%S")


def create_booking_request(booking_data, api_client, auth_headers=None):
    """Helper para crear un booking mediante petición HTTP."""

    logger.info("Intentando crear booking con datos: %s",
                json.dumps(booking_data, ensure_ascii=False))

    # Preparar headers
    headers = {}
    if auth_headers:
        headers.update(auth_headers)

    # Ejecutar petición HTTP
    start_time = time.time()
    response = api_client.make_request(
        endpoint="bookings",
        method="POST",
        data=booking_data, 
        headers=headers
    )
    duration = time.time() - start_time

    logger.info("Status Code: %d | Duración: %.3fs",
                response.status_code, duration)
    logger.debug("Response: %s",
                 response.text[:200] if response.text else "Sin contenido")

    return response

    




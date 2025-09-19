import pytest
from http import HTTPStatus
import random
import string
import logging
import time

logger = logging.getLogger(__name__)


class AirportsPage:
    def __init__(self, api_client):
        self.api_client = api_client
        self.endpoint = "airports"  # No dejar la URL completa ni visible

    def create_airport(self, airport_data, headers):
        return self.api_client.make_request(
            method="POST",
            endpoint=self.endpoint,
            data=airport_data,
            headers=headers
        )


# Escenario exitoso
@pytest.mark.parametrize("city,country", [
    ("City 1", "Country 1"),
    ("City 2", "Country 2")
])
def test_create_airport_success(api_client, auth_headers, city, country):
    airports_page = AirportsPage(api_client)
    iata_code = ''.join(random.choices(string.ascii_uppercase, k=3))
    airport_data = {
        "iata_code": iata_code,
        "city": city,
        "country": country
    }
    start = time.time()
    response = airports_page.create_airport(airport_data, auth_headers)
    duration = time.time() - start
    if response.status_code != HTTPStatus.CREATED:
        logger.error(
            f"[test_create_airport_success] Contexto: city={city}, country={country}, iata_code={iata_code} | "
            f"Status esperado: 201, recibido: {response.status_code} | "
            f"Datos enviados: {airport_data} | Headers: {auth_headers} | "
            f"Duración: {duration:.2f}s | "
            f"Respuesta: {response.text}"
        )
    assert response.status_code == HTTPStatus.CREATED
    resp_json = response.json()
    assert resp_json["iata_code"] == iata_code
    assert resp_json["city"] == city
    assert resp_json["country"] == country


# Faltan campos obligatorios
@pytest.mark.parametrize("airport_data,missing_field", [
    ({"city": "City", "country": "Country"}, "iata_code"),
    ({"iata_code": "ABC", "country": "Country"}, "city"),
    ({"iata_code": "ABC", "city": "City"}, "country")
])
def test_create_airport_missing_fields(api_client, auth_headers, airport_data, missing_field):
    airports_page = AirportsPage(api_client)
    start = time.time()
    response = airports_page.create_airport(airport_data, auth_headers)
    duration = time.time() - start
    if response.status_code != 422:
        logger.error(
            f"[test_create_airport_missing_fields] Contexto: missing_field={missing_field}, airport_data={airport_data} | "
            f"Status esperado: 422, recibido: {response.status_code} | "
            f"Headers: {auth_headers} | Duración: {duration:.2f}s | "
            f"Respuesta: {response.text}"
        )
    assert response.status_code == 422
    resp_json = response.json()
    if not any(missing_field in str(item) for item in resp_json.get("detail", [])):
        logger.error(
            f"[test_create_airport_missing_fields] Contexto: missing_field={missing_field}, airport_data={airport_data} | "
            f"No se encontró el error esperado en la respuesta | Respuesta: {response.text}"
        )
    assert any(missing_field in str(item) for item in resp_json.get("detail", []))


# iata_code longitud incorrecta
@pytest.mark.parametrize("iata_code", ["AB", "ABCD", "A", "ABCDE"])
def test_create_airport_invalid_iata_length(api_client, auth_headers, iata_code):
    airports_page = AirportsPage(api_client)
    airport_data = {
        "iata_code": iata_code,
        "city": "City",
        "country": "Country"
    }
    start = time.time()
    response = airports_page.create_airport(airport_data, auth_headers)
    duration = time.time() - start
    if response.status_code != 422:
        logger.error(
            f"[test_create_airport_invalid_iata_length] Contexto: iata_code={iata_code}, airport_data={airport_data} | "
            f"Status esperado: 422, recibido: {response.status_code} | "
            f"Headers: {auth_headers} | Duración: {duration:.2f}s | "
            f"Respuesta: {response.text}"
        )
    assert response.status_code == 422
    resp_json = response.json()
    if not any("iata_code" in str(item) for item in resp_json.get("detail", [])):
        logger.error(
            f"[test_create_airport_invalid_iata_length] Contexto: iata_code={iata_code}, airport_data={airport_data} | "
            f"No se encontró el error esperado en la respuesta | Respuesta: {response.text}"
        )
    assert any("iata_code" in str(item) for item in resp_json.get("detail", []))


# iata_code con caracteres no permitidos
@pytest.mark.parametrize("iata_code", ["A1C", "A-C", "abc", "123", "A*C"])
def test_create_airport_invalid_iata_format(api_client, auth_headers, iata_code):
    airports_page = AirportsPage(api_client)
    airport_data = {
        "iata_code": iata_code,
        "city": "City",
        "country": "Country"
    }
    start = time.time()
    response = airports_page.create_airport(airport_data, auth_headers)
    duration = time.time() - start
    if response.status_code != 422:
        logger.error(
            f"[test_create_airport_invalid_iata_format] Contexto: iata_code={iata_code}, airport_data={airport_data} | "
            f"Status esperado: 422, recibido: {response.status_code} | "
            f"Headers: {auth_headers} | Duración: {duration:.2f}s | "
            f"Respuesta: {response.text}"
        )
    assert response.status_code == 422
    resp_json = response.json()
    if not any("iata_code" in str(item) for item in resp_json.get("detail", [])):
        logger.error(
            f"[test_create_airport_invalid_iata_format] Contexto: iata_code={iata_code}, airport_data={airport_data} | "
            f"No se encontró el error esperado en la respuesta | Respuesta: {response.text}"
        )
    assert any("iata_code" in str(item) for item in resp_json.get("detail", []))


# Campos adicionales no permitidos
@pytest.mark.parametrize("extra_field", ["name", "extra", "airport_id"])
def test_create_airport_extra_fields(api_client, auth_headers, extra_field):
    airports_page = AirportsPage(api_client)
    iata_code = ''.join(random.choices(string.ascii_uppercase, k=3))
    airport_data = {
        "iata_code": iata_code,
        "city": "City",
        "country": "Country",
        extra_field: "valor"
    }
    start = time.time()
    response = airports_page.create_airport(airport_data, auth_headers)
    duration = time.time() - start
    if response.status_code != 422:
        logger.error(
            f"[test_create_airport_extra_fields] Contexto: extra_field={extra_field}, airport_data={airport_data} | "
            f"Status esperado: 422, recibido: {response.status_code} | "
            f"Headers: {auth_headers} | Duración: {duration:.2f}s | "
            f"Respuesta: {response.text}"
        )
    assert response.status_code == 422, (
        f"BUG: La API aceptó un campo adicional '{extra_field}' y respondió con {response.status_code} en vez de 422. "
        f"Respuesta: {response.text}"
    )
    resp_json = response.json()
    if not any("additionalProperties" in str(item) for item in resp_json.get("detail", [])):
        logger.error(
            f"[test_create_airport_extra_fields] Contexto: extra_field={extra_field}, airport_data={airport_data} | "
            f"No se encontró el error esperado en la respuesta | Respuesta: {response.text}"
        )
    assert any("additionalProperties" in str(item) for item in resp_json.get("detail", [])), (
        f"BUG: La API no reportó error por propiedades adicionales. Respuesta: {response.text}"
    )


# Duplicidad de iata_code
@pytest.mark.parametrize("city,country", [
    ("City 3", "Country 3")
])
def test_create_airport_duplicate_iata(api_client, auth_headers, city, country):
    airports_page = AirportsPage(api_client)
    iata_code = ''.join(random.choices(string.ascii_uppercase, k=3))
    airport_data = {
        "iata_code": iata_code,
        "city": city,
        "country": country
    }
    start = time.time()
    response1 = airports_page.create_airport(airport_data, auth_headers)
    duration1 = time.time() - start
    if response1.status_code != HTTPStatus.CREATED:
        logger.error(
            f"[test_create_airport_duplicate_iata] Contexto: city={city}, country={country}, iata_code={iata_code} | "
            f"Status esperado: 201, recibido: {response1.status_code} | "
            f"Datos enviados: {airport_data} | Headers: {auth_headers} | "
            f"Duración: {duration1:.2f}s | "
            f"Respuesta: {response1.text}"
        )
    assert response1.status_code == HTTPStatus.CREATED
    start2 = time.time()
    response2 = airports_page.create_airport(airport_data, auth_headers)
    duration2 = time.time() - start2
    if response2.status_code not in [400, 409]:
        logger.error(
            f"[test_create_airport_duplicate_iata] Contexto: city={city}, country={country}, iata_code={iata_code} | "
            f"Status esperado: 400/409, recibido: {response2.status_code} | "
            f"Datos enviados: {airport_data} | Headers: {auth_headers} | "
            f"Duración: {duration2:.2f}s | "
            f"Respuesta: {response2.text}"
        )
    assert response2.status_code in [400, 409]


# Campos vacíos
@pytest.mark.parametrize("airport_data,empty_field", [
    ({"iata_code": "ABC", "city": "", "country": "Country"}, "city"),
    ({"iata_code": "ABC", "city": "City", "country": ""}, "country")
])
def test_create_airport_empty_fields(api_client, auth_headers, airport_data, empty_field):
    airports_page = AirportsPage(api_client)
    start = time.time()
    response = airports_page.create_airport(airport_data, auth_headers)
    duration = time.time() - start
    if response.status_code != 422:
        logger.error(
            f"[test_create_airport_empty_fields] Contexto: empty_field={empty_field}, airport_data={airport_data} | "
            f"Status esperado: 422, recibido: {response.status_code} | "
            f"Headers: {auth_headers} | Duración: {duration:.2f}s | "
            f"Respuesta: {response.text}"
        )
    assert response.status_code == 422
    resp_json = response.json()
    if not any(empty_field in str(item) for item in resp_json.get("detail", [])):
        logger.error(
            f"[test_create_airport_empty_fields] Contexto: empty_field={empty_field}, airport_data={airport_data} | "
            f"No se encontró el error esperado en la respuesta | Respuesta: {response.text}"
        )
    assert any(empty_field in str(item) for item in resp_json.get("detail", []))


# Formato incorrecto de datos
@pytest.mark.parametrize("airport_data,invalid_field", [
    ({"iata_code": 123, "city": "City", "country": "Country"}, "iata_code"),
    ({"iata_code": "ABC", "city": 456, "country": "Country"}, "city"),
    ({"iata_code": "ABC", "city": "City", "country": 789}, "country")
])
def test_create_airport_invalid_field_type(api_client, auth_headers, airport_data, invalid_field):
    airports_page = AirportsPage(api_client)
    start = time.time()
    response = airports_page.create_airport(airport_data, auth_headers)
    duration = time.time() - start
    if response.status_code != 422:
        logger.error(
            f"[test_create_airport_invalid_field_type] Contexto: invalid_field={invalid_field}, airport_data={airport_data} | "
            f"Status esperado: 422, recibido: {response.status_code} | "
            f"Headers: {auth_headers} | Duración: {duration:.2f}s | "
            f"Respuesta: {response.text}"
        )
    assert response.status_code == 422
    resp_json = response.json()
    if not any(invalid_field in str(item) for item in resp_json.get("detail", [])):
        logger.error(
            f"[test_create_airport_invalid_field_type] Contexto: invalid_field={invalid_field}, airport_data={airport_data} | "
            f"No se encontró el error esperado en la respuesta | Respuesta: {response.text}"
        )
    assert any(invalid_field in str(item) for item in resp_json.get("detail", []))

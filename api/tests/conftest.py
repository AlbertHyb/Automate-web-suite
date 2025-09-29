import os
import pytest
from config.settings import Config
from api.api_helper import ApiHelper
import requests
import time
from http import HTTPStatus
import logging
from api.tests.airports.list_airports import fetch_data
from api.pages.flights_page import create_flight_request  # actualizado
from api.tests.aircfrafts.create_aircraft import create_aircraft_request
import time
from api.tests.aircfrafts.create_aircraft import create_aircraft_request


# =============================================================
# Logging simplificado (reversión a esquema básico)
# =============================================================
# Motivo: La versión anterior con RotatingFileHandler y múltiples handlers
# produjo situaciones donde Pytest mostraba tests como ignorados (duplicación
# de handlers en ejecuciones paralelas y posible interferencia con salida).
# Se vuelve a un setup mínimo y estable.

def configure_logging():
    if logging.getLogger().handlers:
        return  # Ya configurado por un proceso previo (evita duplicados)
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'tests.log')
    level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logging.getLogger(__name__).info(f"Logging básico inicializado nivel={level_name} archivo={log_file}")

configure_logging()
logger = logging.getLogger(__name__)

# Configuración
config = Config()

BASE_URL = "https://cf-automation-airline-api.onrender.com"

@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL

@pytest.fixture(scope="module")
def api_client(base_url):
    """Fixture centralizado para crear un cliente de API para las pruebas."""
    api_client = ApiHelper(base_url)

    if not api_client.is_service_up():
        pytest.skip("El servicio API no está disponible")
    print("Servicio API disponible")

    return api_client

@pytest.fixture(scope="session")
def admin_token() -> str:
    creds = Config.get_auth_credentials()
    username = creds["username"]
    password = creds["password"]
    login_data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "scope": "read write",
        "client_id": "test_client",
        "client_secret": "test_secret"
    }

    try:
        print("\nIntentando login de admin...")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"Login response ({response.status_code}): {response.text}")

        if response.status_code != 200:
            pytest.fail(f"Error en login de admin: {response.text}")

        token = response.json().get("access_token")
        if not token or not isinstance(token, str):
            pytest.fail("No se encontró el token en la respuesta o el token no es tipo str")

        print("Login de admin exitoso")
        return str(token)

    except Exception as e:
        pytest.fail(f"Error al obtener el token de admin: {str(e)}")

@pytest.fixture(scope="function")
def test_user(api_client):
    """Crea un usuario de prueba único y retorna su user_id y token."""
    import time
    signup_data = Config.get_signup_status_data()
    unique_email = f"test_user_{int(time.time() * 1000)}@gmail.com"
    signup_data["email"] = unique_email
    response = api_client.make_request(
        endpoint="auth/signup",
        method="POST",
        data=signup_data
    )
    assert response.status_code in (200, 201), f"No se pudo crear usuario de prueba. Respuesta: {response.text}"
    user_id = response.json().get("uid")
    # Login para obtener el token
    login_data = {
        "username": unique_email,
        "grant_type": "password",
        "password": signup_data["password"],
        "scope": "read write",
        "client_id": "test_client",
        "client_secret": "test_secret"
    }

    login_response = api_client.make_request(
        endpoint="auth/login",
        method="POST",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        use_form_data=True
    )
    assert login_response.status_code == 200, f"No se pudo hacer login del usuario de prueba. Respuesta: {login_response.text}"
    token = login_response.json().get("access_token")
    return {
        "uid": user_id,
        "token": token,
        "email": unique_email,
        "password": signup_data["password"]
    }


@pytest.fixture
def auth_signup(api_client):
    """Crea un usuario de prueba y retorna sus datos y token."""
    timestamp = int(time.time())
    email = f"fernandohz{timestamp}@gmail.com"
    password = "Cafe&Libro456?"
    full_name = "Fernando Hernandez"
    test_data = {
        "email": email,
        "password": password,
        "full_name": full_name
    }
    # Crear usuario
    signup_resp = api_client.make_request(
        method="POST",
        endpoint="auth/signup",
        data=test_data
    )
    assert signup_resp.status_code == HTTPStatus.CREATED
    user_id = signup_resp.json().get("id")

    # Login para obtener el token
    login_data = {
        "username": email,
        "password": password,
        "grant_type": "password",
        "scope": "read write",
        "client_id": "test_client",
        "client_secret": "test_secret"
    }
    login_resp = api_client.make_request(
        method="POST",
        endpoint="auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        use_form_data=True
    )
    assert login_resp.status_code == HTTPStatus.OK
    access_token = login_resp.json().get("access_token")

    return {
        "user_id": user_id,
        "access_token": access_token,
        "email": email,
        "password": password,
        "full_name": full_name
    }

# -------------------------------------------------
# Hook anterior eliminado (causaba re-ejecución) - se deja comentado
# -------------------------------------------------
# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     """Hook para generar reportes cuando hay fallos (DESACTIVADO).
#     Razón: relanzar pytest dentro del summary puede causar estados inesperados
#     y que tests aparezcan como ignorados/doble ejecución."""
#     pass

# Hook para capturar outcome del test

# Sustituir implementación previa (causaba AttributeError en Pytest 8)
import pytest as _pytest_mod
@_pytest_mod.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Ejecutar el resto de hooks primero
    outcome = yield
    rep = outcome.get_result()
    # Guardar el reporte en el item para acceso posterior
    setattr(item, f"rep_{rep.when}", rep)

# Fixture autouse para loggear inicio y fin de cada test con duración
import time as _time_mod
@pytest.fixture(autouse=True)
def log_test_start_end(request):
    start = _time_mod.time()
    logger.info(f"[TEST_START] nodeid={request.node.nodeid}")
    yield
    duration = _time_mod.time() - start
    # Determinar outcome real si existe rep_call
    outcome = 'unknown'
    rep_call = getattr(request.node, 'rep_call', None)
    if rep_call:
        outcome = rep_call.outcome
    logger.info(f"[TEST_END] nodeid={request.node.nodeid} outcome={outcome} duration={duration:.3f}s")

# --------------------------------------------
# Resource Tracker para limpiar recursos creados
# --------------------------------------------
class ResourceTracker:
    """Registra recursos creados durante un test y los elimina al finalizar."""
    endpoint_map = {
        'aircraft': 'aircrafts',
        'aircrafts': 'aircrafts',
        'flight': 'flights',
        'flights': 'flights'
    }

    def __init__(self, api_client, auth_headers, logger):
        self.api_client = api_client
        self.auth_headers = auth_headers
        self.logger = logger
        self._resources = []  # (resource_type, resource_id)

    def register(self, resource_type: str, resource_id: str):
        if not resource_type or not resource_id:
            return
        self._resources.append((resource_type, resource_id))
        self.logger.debug(f"[RESOURCE_REGISTER] type={resource_type} id={resource_id}")

    def cleanup(self):
        for r_type, r_id in reversed(self._resources):
            endpoint_base = self.endpoint_map.get(r_type)
            if not endpoint_base:
                self.logger.warning(f"[RESOURCE_CLEANUP_SKIP] tipo desconocido={r_type} id={r_id}")
                continue
            try:
                resp = self.api_client.make_request(
                    method="DELETE",
                    endpoint=f"{endpoint_base}/{r_id}",
                    headers=self.auth_headers
                )
                if resp.status_code in (200, 202, 204):
                    self.logger.info(f"[RESOURCE_DELETED] type={r_type} id={r_id} status={resp.status_code}")
                else:
                    self.logger.warning(
                        f"[RESOURCE_DELETE_FAILED] type={r_type} id={r_id} status={resp.status_code} body={resp.text[:200]}"
                    )
            except Exception as e:
                self.logger.warning(f"[RESOURCE_DELETE_EXCEPTION] type={r_type} id={r_id} error={e}")
        self._resources.clear()

@pytest.fixture
def resource_tracker(api_client, auth_headers):
    tracker = ResourceTracker(api_client, auth_headers, logger)
    yield tracker
    tracker.cleanup()

@pytest.fixture
def static_airport():
    return {
        "id": 1,
        "name": "John F. Kennedy International Airport",
        "code": "JFK",
        "city": "New York",
        "country": "USA",
        "latitude": 40.6413,
        "longitude": -73.7781,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }

@pytest.fixture(scope="session")
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture(scope="module")
def airport_test_data(api_client):
    list_response = fetch_data(skip=0, limit=30, api_client=api_client)

    if list_response.status_code != 200:
        pytest.skip("No se pudo obtener la lista de aeropuertos para las pruebas")

    airports = list_response.json()

    if not airports or len(airports) == 0:
        pytest.skip("No hay aeropuertos disponibles para las pruebas")

    logger.info(f"Aeropuertos disponibles para pruebas: {[a['iata_code'] for a in airports[:5]]}")

    invalid_iata = "ZZZ" if "ZZZ" not in [a["iata_code"] for a in airports] else "XXX"

    return {
        "airports": airports,
        "valid_iata": airports[0]["iata_code"],
        "invalid_iata": invalid_iata
    }

@pytest.fixture(scope="module")
def flight_positive_data(api_client, auth_headers, airport_test_data, resource_tracker):
    airports = airport_test_data["airports"]
    if len(airports) < 2:
        pytest.skip("No hay aeropuertos suficientes para crear vuelo positivo")
    origin = airports[0]["iata_code"]
    destination = airports[1]["iata_code"] if airports[1]["iata_code"] != origin else airports[-1]["iata_code"]

    aircraft_payload = {
        "tail_number": str(int(time.time() * 1000)),
        "model": "Boeing",
        "capacity": 180
    }
    aircraft_resp = create_aircraft_request(aircraft_payload, api_client, auth_headers)
    assert aircraft_resp.status_code == 201, f"No se pudo crear aircraft para vuelo positivo. Resp: {aircraft_resp.text}"
    aircraft_id = aircraft_resp.json().get("id")
    assert aircraft_id, "Respuesta de creación de aircraft no contiene 'id'"
    resource_tracker.register('aircraft', aircraft_id)

    from datetime import timezone, timedelta, datetime as _dt
    departure = (_dt.now(timezone.utc) + timedelta(days=3)).replace(microsecond=0)
    arrival = departure + timedelta(hours=2)
    flight_payload = {
        "origin": origin,
        "destination": destination,
        "departure_time": departure.isoformat(),
        "arrival_time": arrival.isoformat(),
        "base_price": 1500.0,
        "aircraft_id": aircraft_id
    }
    flight_resp = create_flight_request(flight_payload, api_client, auth_headers)
    assert flight_resp.status_code in (200, 201), f"Fallo al crear vuelo positivo. Status={flight_resp.status_code} Body={flight_resp.text}"
    try:
        flight_id = flight_resp.json().get("id") or flight_resp.json().get("flight_id")
        if flight_id:
            resource_tracker.register('flight', flight_id)
    except Exception:
        logger.warning("No se pudo extraer flight_id de la respuesta de creación de vuelo para cleanup.")

    search_params = {
        "origin": origin,
        "destination": destination,
        "date": departure.date().isoformat(),
        "skip": 0,
        "limit": 10
    }
    return search_params

import time
from api.tests.aircfrafts.create_aircraft import create_aircraft_request

@pytest.fixture(scope="module")
def aircraft_id(api_client, auth_headers):
    """Crea un avión y retorna su ID para pruebas dependientes."""
    payload = {
        "tail_number": str(int(time.time() * 1000))[:10],  # Ajustar longitud máxima a 10 caracteres
        "model": "Boeing",
        "capacity": 180
    }
    response = create_aircraft_request(payload, api_client, auth_headers)
    assert response.status_code == 201, (
        f"Fallo al crear avión. Status={response.status_code}, Body={response.text}"
    )
    try:
        aircraft_id = response.json().get("id")
        assert aircraft_id, "La respuesta de creación no contiene 'id'"
        return aircraft_id
    except Exception as e:
        pytest.fail(f"Error al extraer 'id' del avión creado: {str(e)}")

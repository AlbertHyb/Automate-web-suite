import requests
import logging
import time
from typing import Optional, Dict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class ApiHelper:
    """Cliente HTTP centralizado y mejorado para operaciones de API."""

    def __init__(self, base_url: str, timeout: int = 4, max_retries: int = 3):
        """
        Inicializa el helper de API con sesión persistente.
        Args:
            base_url: URL base de la API
            timeout: Timeout en segundos para requests
            max_retries: Número máximo de reintentos automáticos
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

        # Configurar estrategia de reintentos
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,  # Espera 1s, 2s, 4s entre reintentos
            # Códigos que disparan retry
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Headers por defecto
        self.session.headers.update({
            'User-Agent': 'AutomateWebSuite-API-Tests/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def is_service_up(self, max_attempts: int = 3, delay: int = 2) -> bool:
        endpoints_to_check = ['/docs', '/health', '/']

        for attempt in range(max_attempts):
            for endpoint in endpoints_to_check:
                try:
                    response = self.session.get(
                        f"{self.base_url}{endpoint}",
                        timeout=5
                    )
                    # 404 también indica que el servidor responde
                    if response.status_code in [200, 404]:
                        logger.info("Servicio API disponible en %s", endpoint)
                        return True
                except requests.RequestException as e:
                    logger.debug(
                        "Intento %d/%d en %s falló: %s",
                        attempt + 1, max_attempts, endpoint, e)

            if attempt < max_attempts - 1:
                logger.warning(
                    "Servicio no disponible, reintentando en %ss...", delay)
                time.sleep(delay)

        logger.error(
            "Servicio API no disponible después de todos los intentos")
        return False

    def set_auth_token(self, token: str):
        self.session.headers.update({'Authorization': f'Bearer {token}'})
        logger.info("Token de autenticación configurado")

    def clear_auth_token(self):
        """Elimina el token de autenticación."""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
            logger.info("Token de autenticación eliminado")

    def set_header(self, key: str, value: str):
        """Configura un header personalizado."""
        self.session.headers.update({key: value})

    def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        use_form_data: bool = False,
        expected_status: Optional[int] = None,
        timeout: Optional[int] = None
    ) -> requests.Response:

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        method = method.upper()
        timeout = timeout or self.timeout

        # Merge headers
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)

        # Log del request
        logger.info("%s %s", method, url)
        if data:
            logger.debug("   Payload: %s", data)

        try:
            start_time = time.time()

            # Realizar la petición según el método
            if method == "GET":
                response = self.session.get(
                    url,
                    params=data,
                    headers=request_headers,
                    timeout=timeout
                )

            elif method == "POST":
                if use_form_data:
                    request_headers['Content-Type'] = 'application/x-www-form-urlencoded'
                    response = self.session.post(
                        url,
                        data=data,
                        headers=request_headers,
                        timeout=timeout
                    )
                else:
                    response = self.session.post(
                        url,
                        json=data,
                        headers=request_headers,
                        timeout=timeout
                    )

            elif method == "PUT":
                if use_form_data:
                    request_headers['Content-Type'] = 'application/x-www-form-urlencoded'
                    response = self.session.put(
                        url,
                        data=data,
                        headers=request_headers,
                        timeout=timeout
                    )
                else:
                    response = self.session.put(
                        url,
                        json=data,
                        headers=request_headers,
                        timeout=timeout
                    )

            elif method == "DELETE":
                response = self.session.delete(
                    url,
                    json=data if data else None,
                    headers=request_headers,
                    timeout=timeout
                )

            elif method == "PATCH":
                if use_form_data:
                    request_headers['Content-Type'] = 'application/x-www-form-urlencoded'
                    response = self.session.patch(
                        url,
                        data=data,
                        headers=request_headers,
                        timeout=timeout
                    )
                else:
                    response = self.session.patch(
                        url,
                        json=data,
                        headers=request_headers,
                        timeout=timeout
                    )

            else:
                raise ValueError(f"Método HTTP no soportado: {method}")

            # Calcular tiempo de respuesta
            elapsed = round((time.time() - start_time) * 1000, 2)

            # Log de la respuesta
            logger.info("   Status: %s in %sms", response.status_code, elapsed)

            # Log del body en caso de error
            if not response.ok:
                logger.error("   Error Response: %s", response.text[:500])
            else:
                logger.debug("   Response: %s", response.text[:200])

            # Validar status code si se especificó
            if expected_status is not None:
                assert response.status_code == expected_status, \
                    "Expected status %s, got %s. Response: %s" % (
                        expected_status, response.status_code, response.text)

            return response

        except requests.ConnectionError as e:
            error_msg = "No se pudo conectar a %s: %s"
            logger.error(error_msg, url, str(e))
            raise RuntimeError(error_msg % (url, str(e))) from e

        except requests.Timeout as e:
            error_msg = "Timeout (%ss) en %s: %s"
            logger.error(error_msg, timeout, url, str(e))
            raise RuntimeError(error_msg % (timeout, url, str(e))) from e

        except AssertionError:
            raise  # Re-lanzar AssertionError sin modificar

        except Exception as e:
            error_msg = "Error inesperado en %s: %s"
            logger.error(error_msg, url, str(e))
            raise RuntimeError(error_msg % (url, str(e))) from e

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Realiza una petición GET."""
        return self.make_request(endpoint, method="GET", data=params, **kwargs)

    def post(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Realiza una petición POST."""
        return self.make_request(endpoint, method="POST", data=data, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Realiza una petición PUT."""
        return self.make_request(endpoint, method="PUT", data=data, **kwargs)

    def delete(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Realiza una petición DELETE."""
        return self.make_request(endpoint, method="DELETE", data=data, **kwargs)

    def patch(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Realiza una petición PATCH."""
        return self.make_request(endpoint, method="PATCH", data=data, **kwargs)

    def get_health_check(self) -> requests.Response:
        """Realiza un health check del servicio."""
        return self.get("health")

    def get_api_docs(self) -> requests.Response:
        """Obtiene la documentación de la API."""
        return self.get("docs")

    def validate_response_schema(self, response: requests.Response, schema: Dict) -> bool:
    
        try:
            data = response.json()
        except (ValueError, requests.exceptions.JSONDecodeError) as e:
            logger.error("Respuesta no es JSON válido: %s", e)
            return False

        for key in schema.keys():
            if key not in data:
                logger.error("Campo '%s' faltante en respuesta", key)
                return False

        return True

    def close(self):
        """Cierra la sesión HTTP."""
        self.session.close()
        logger.info("Sesión HTTP cerrada")

    def __enter__(self):
        """Soporte para context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra automáticamente la sesión al salir del contexto."""
        self.close()

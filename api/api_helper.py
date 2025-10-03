import requests
import logging

logger = logging.getLogger(__name__)

class ApiHelper:
    """Cliente HTTP centralizado para todas las operaciones de API."""

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def is_service_up(self):
        """Verifica si el servicio API está disponible."""
        try:
            response = requests.get(f"{self.base_url}/docs")
            return response.status_code == 200
        except Exception:
            return False

    def make_request(self, endpoint, method="GET", data=None, headers=None, use_form_data=False):
        """Realiza una petición HTTP a la API.

        Args:
            endpoint: Endpoint de la API (sin slash inicial)
            method: Método HTTP (GET, POST, PUT, DELETE)
            data: Datos a enviar (dict para JSON, o form data)
            headers: Headers HTTP adicionales
            use_form_data: Si True, envía como form-data en lugar de JSON

        Returns:
            requests.Response: Respuesta de la API

        Raises:
            RuntimeError: Si no se puede conectar a la API
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if headers is None:
            headers = {}

        try:
            method = method.upper()

            if method == "GET":
                # GET requests use params for query parameters
                response = requests.get(url, params=data, headers=headers)

            elif method == "POST":
                if use_form_data:
                    headers = {**headers, "Content-Type": "application/x-www-form-urlencoded"}
                    response = requests.post(url, data=data, headers=headers)
                else:
                    response = requests.post(url, json=data, headers=headers)

            elif method == "PUT":
                if use_form_data:
                    headers = {**headers, "Content-Type": "application/x-www-form-urlencoded"}
                    response = requests.put(url, data=data, headers=headers)
                else:
                    response = requests.put(url, json=data, headers=headers)

            elif method == "DELETE":
                # DELETE can have a body (json) or just headers
                if data:
                    response = requests.delete(url, json=data, headers=headers)
                else:
                    response = requests.delete(url, headers=headers)

            elif method == "PATCH":
                # Support for PATCH method (partial updates)
                if use_form_data:
                    headers = {**headers, "Content-Type": "application/x-www-form-urlencoded"}
                    response = requests.patch(url, data=data, headers=headers)
                else:
                    response = requests.patch(url, json=data, headers=headers)

            else:
                raise ValueError(f"Método HTTP no soportado: {method}")

            # Log the request for debugging
            logger.debug(f"[API_REQUEST] {method} {url} - Status: {response.status_code}")

            return response

        except requests.ConnectionError as e:
            error_msg = f"No se pudo conectar a la API en {url}: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        except requests.Timeout as e:
            error_msg = f"Timeout en la petición a {url}: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        except Exception as e:
            error_msg = f"Error inesperado en petición a {url}: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def get_health_check(self):
        """Realiza un health check básico del servicio."""
        return self.make_request("health", method="GET")

    def get_api_docs(self):
        """Obtiene la documentación de la API (Swagger/OpenAPI)."""
        return self.make_request("docs", method="GET")

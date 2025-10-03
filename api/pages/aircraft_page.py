import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class AircraftPage:
    """Para operaciones de aviones.
    Centraliza todas las operaciones relacionadas con el endpoint /aircrafts
    """

    def __init__(self, api_client):
        self.api_client = api_client
        self.endpoint = "aircrafts"

    def create_aircraft(self, aircraft_data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> object:
        """Crea un nuevo avión.

        Args:
            aircraft_data: Datos del avión (tail_number, model, capacity)
            headers: Headers HTTP opcionales

        Returns:
            requests.Response: Respuesta de la API
        """
        default_headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if headers:
            default_headers.update(headers)

        return self.api_client.make_request(
            method="POST",
            endpoint=self.endpoint,
            data=aircraft_data,
            headers=default_headers
        )

    def get_aircraft_by_id(self, aircraft_id: str, headers: Optional[Dict[str, str]] = None) -> object:
        """Obtiene un avión por su ID.

        Args:
            aircraft_id: ID del avión
            headers: Headers HTTP opcionales

        Returns:
            requests.Response: Respuesta de la API
        """
        default_headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if headers:
            default_headers.update(headers)

        endpoint_full = f"{self.endpoint}/{aircraft_id}"
        return self.api_client.make_request(
            method="GET",
            endpoint=endpoint_full,
            data=None,
            headers=default_headers
        )

    def list_aircrafts(self, headers: Optional[Dict[str, str]] = None, skip: int = 0, limit: int = 100) -> object:
        """Lista todos los aviones con paginación.

        Args:
            headers: Headers HTTP opcionales
            skip: Número de elementos a saltar
            limit: Límite de elementos a retornar

        Returns:
            requests.Response: Respuesta de la API
        """
        default_headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if headers:
            default_headers.update(headers)

        params = {"skip": skip, "limit": limit}
        endpoint_with_params = f"{self.endpoint}?skip={skip}&limit={limit}"

        return self.api_client.make_request(
            method="GET",
            endpoint=endpoint_with_params,
            headers=default_headers
        )

    def update_aircraft(self, aircraft_id: str, aircraft_data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> object:
        """Actualiza un avión existente.
        Args:
            aircraft_id: ID del avión a actualizar
            aircraft_data: Nuevos datos del avión
            headers: Headers HTTP opcionales
        Returns:
            requests.Response: Respuesta de la API
        """
        default_headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if headers:
            default_headers.update(headers)

        endpoint_full = f"{self.endpoint}/{aircraft_id}"
        return self.api_client.make_request(
            method="PUT",
            endpoint=endpoint_full,
            data=aircraft_data,
            headers=default_headers
        )

    def delete_aircraft(self, aircraft_id: str, headers: Optional[Dict[str, str]] = None) -> object:
        """Elimina un avión.

        Args:
            aircraft_id: ID del avión a eliminar
            headers: Headers HTTP opcionales

        Returns:
            requests.Response: Respuesta de la API
        """
        default_headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if headers:
            default_headers.update(headers)

        endpoint_full = f"{self.endpoint}/{aircraft_id}"
        return self.api_client.make_request(
            method="DELETE",
            endpoint=endpoint_full,
            headers=default_headers
        )

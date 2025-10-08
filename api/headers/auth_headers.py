"""
Headers específicos para endpoints de autenticación.
Sigue el patrón Page Object Model para separar la configuración de headers.
"""

from typing import Dict


class AuthHeaders:
    """Headers específicos para operaciones de autenticación."""
    
    @staticmethod
    def get_signup_headers() -> Dict[str, str]:
        """Headers para el endpoint de registro de usuarios."""
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    @staticmethod
    def get_login_headers() -> Dict[str, str]:
        """Headers para el endpoint de login."""
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
    
    @staticmethod
    def get_auth_headers(token: str) -> Dict[str, str]:
        """Headers para endpoints que requieren autenticación."""
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    @staticmethod
    def get_json_headers() -> Dict[str, str]:
        """Headers genéricos para operaciones JSON."""
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    @staticmethod
    def get_form_data_headers() -> Dict[str, str]:
        """Headers para operaciones con form data."""
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

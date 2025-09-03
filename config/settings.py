"""
Configuración centralizada de la aplicación.
Lee variables de entorno y proporciona valores por defecto seguros.
"""

import os
from typing import Dict
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Clase para manejar la configuración de la aplicación"""
    
    @staticmethod
    def get_base_url() -> str:
        """Construye la URL base de forma segura"""
        protocol = os.getenv('API_PROTOCOL', 'https')
        host = os.getenv('API_HOST')
        base_path = os.getenv('API_BASE_PATH', '/')
        version = os.getenv('API_VERSION')
        
        if not host:
            raise ValueError("API_HOST no está configurado en las variables de entorno")
            
        url = f"{protocol}://{host}".rstrip('/')

        # Asegura que base_path y version tengan la barra correcta
        if base_path:
            if not base_path.startswith('/'):
                base_path = '/' + base_path
            if base_path != '/':
                url += base_path.rstrip('/')

        if version:
            if not version.startswith('/'):
                version = '/' + version
            url += version

        return url.rstrip('/')
    
    @staticmethod
    def get_auth_credentials() -> Dict[str, str]:
        """Obtiene las credenciales de autenticación"""
        username = os.getenv('ADMIN_USER')
        password = os.getenv('ADMIN_PASS')
        
        if not username or not password:
            raise ValueError("Credenciales de administrador no configuradas")
            
        return {
            "username": username,
            "password": password
        }
    
    @staticmethod
    def get_request_timeout() -> int:
        """Obtiene el timeout para requests"""
        return int(os.getenv('REQUEST_TIMEOUT', '5'))
    
    @staticmethod
    def get_rate_limit_retry() -> int:
        """Obtiene el número de reintentos para rate limiting"""
        return int(os.getenv('RATE_LIMIT_RETRY', '3'))

    @staticmethod
    def get_signup_status_data() -> Dict[str, str]:
        """Obtiene los datos de signup para pruebas de estado del servicio"""
        email = os.getenv('SIGNUP_STATUS_EMAIL', 'test_status_check@gmail.com')
        password = os.getenv('SIGNUP_STATUS_PASS', 'Test1234!')
        full_name = os.getenv('SIGNUP_STATUS_NAME', 'Status Check')
        return {
            "email": email,
            "password": password,
            "full_name": full_name
        }

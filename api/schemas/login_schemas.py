# Esquema para respuesta exitosa de login (código 200)
user_login_success_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "description": "Esquema que valida la respuesta exitosa del endpoint de login",
    "type": "object",
    "properties": {
        "access_token": {
            "type": "string",
            "description": "Token JWT de acceso",
            "minLength": 1
        },
        "token_type": {
            "type": "string",
            "description": "Tipo de token (siempre 'bearer')",
            "enum": ["bearer", "Bearer"]
        },
        "expires_in": {
            "type": "integer",
            "description": "Tiempo de expiración del token en segundos",
            "minimum": 1
        },
        "refresh_token": {
            "type": "string",
            "description": "Token de actualización (opcional)",
            "minLength": 1
        }
    },
    "required": ["access_token", "token_type"],  # Solo estos campos son realmente requeridos en OAuth2
    "additionalProperties": True  # Permitimos propiedades adicionales que la API pueda incluir
}

# Esquema para errores de validación (código 422)
user_login_error_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "description": "Esquema que valida la respuesta de error del endpoint de login",
    "type": "object",
    "properties": {
        "detail": {
            "type": "array",
            "description": "Lista de errores de validación",
            "items": {
                "type": "object",
                "properties": {
                    "loc": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Ubicación del error (campo)"
                    },
                    "msg": {
                        "type": "string",
                        "description": "Mensaje de error"
                    },
                    "type": {
                        "type": "string",
                        "description": "Tipo de error"
                    }
                },
                "required": ["loc", "msg", "type"]
            }
        }
    },
    "required": ["detail"]
}
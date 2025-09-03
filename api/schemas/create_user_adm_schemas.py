# Esquema para respuesta exitosa de creación de usuario (código 201)
create_user_adm_success_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "description": "Esquema que valida la respuesta exitosa de creación de usuario por admin",
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "description": "ID único del usuario creado",
            "pattern": "^usr-[a-zA-Z0-9]+$"
        },
        "email": {
            "type": "string",
            "description": "Email del usuario",
            "format": "email"
        },
        "full_name": {
            "type": "string",
            "description": "Nombre completo del usuario",
            "minLength": 1
        },
        "role": {
            "type": "string",
            "description": "Rol del usuario",
            "enum": ["passenger", "admin"]
        },
        "created_at": {
            "type": "string",
            "description": "Fecha y hora de creación",
            "format": "date-time"
        }
    },
    "required": ["id", "email", "full_name", "role"],
    "additionalProperties": False
}

# Esquema para errores de validación (código 422)
create_user_adm_error_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "description": "Esquema que valida la respuesta de error en creación de usuario",
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

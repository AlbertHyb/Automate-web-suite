# Esquema para la creación exitosa de un aeropuerto
airport_create_success_schema = {
    "type": "object",
    "properties": {
        "iata_code": {"type": "string", "minLength": 3, "maxLength": 3},
        "city": {"type": "string", "minLength": 1},
        "country": {"type": "string", "minLength": 1},
    },
    "required": ["iata_code", "city", "country"],
    "additionalProperties": False,
}

# Esquema para el error 422
airport_create_error_schema = {
    "type": "object",
    "properties": {
        "detail": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "loc": {"type": "array", "items": {"type": "string"}},
                    "msg": {"type": "string"},
                    "type": {"type": "string"},
                },
                "required": ["loc", "msg", "type"],
            },
        },
    },
    "required": ["detail"],
}

flight_search_schema = {
    "type": "object",
    "properties": {
        "origin": {"type": "string", "minLength": 1, "maxLength": 100},
        "destination": {"type": "string", "minLength": 1, "maxLength": 100},
        "date": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"},
        "skip": {"type": "integer", "minimum": 0},
        "limit": {"type": "integer", "minimum": 1, "maximum": 100}
    },
    "required": ["origin", "destination", "date"],
    "additionalProperties": False,
}


flight_search_error_schema = {
    "type": "object",
    "properties": {
        "detail": {
            "oneOf": [
                {"type": "string"},
                {
                    "type": "array",
                    "items": {"type": "object"}
                }
            ]
        }
    },
    "required": ["detail"],
    "additionalProperties": True
}


# Validar antes de enviar

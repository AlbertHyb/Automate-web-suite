airport_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "minimum": 1
        },
        "name": {
            "type": "string",
            "minLength": 1
        },
        "code": {
            "type": "string",
            "pattern": "^[A-Z]{3}$"  # Código IATA de 3 letras
        },
        "city": {
            "type": "string",
            "minLength": 1
        },
        "country": {
            "type": "string",
            "minLength": 1
        },
        "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
        },
        "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
        },
        "created_at": {
            "type": "string",
            "format": "date-time"
        },
        "updated_at": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": ["id", "name", "code", "city", "country"],
    "additionalProperties": False
}
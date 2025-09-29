create_flight_success_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "aircraft_id": {"type": "string"},
        "origin": {"type": "string"},
        "destination": {"type": "string"},
        "departure_time": {"type": "string", "format": "date-time"},
        "arrival_time": {"type": "string", "format": "date-time"},
        "base_price": {"type": "number"},
        "available_seats": {"type": "integer"}
    },
    "required": [
        "id", "aircraft_id", "origin", "destination", "departure_time", "arrival_time", "base_price", "available_seats"
    ]
}

create_flight_201_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "available_seats": {"type": "integer"}
    },
    "required": ["id", "available_seats"]
}

create_flight_error_schema = {
    "type": "object",
    "properties": {
        "detail": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "loc": {"type": "array", "items": {"type": "string"}},
                    "msg": {"type": "string"},
                    "type": {"type": "string"}
                },
                "required": ["loc", "msg", "type"]
            }
        }
    },
    "required": ["detail"]
}

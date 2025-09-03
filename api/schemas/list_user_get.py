list_users_success_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "full_name": {"type": "string"},
            "role": {"type": "string"}
        },
        "required": ["id", "email", "full_name", "role"]
    }
}
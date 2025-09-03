
user_me_get_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "full_name": {"type": "string"},
        "role": {"type": "string", "enum": ["passenger"]}
    },
    "required": ["id", "email", "full_name", "role"],
    "additionalProperties": False
}


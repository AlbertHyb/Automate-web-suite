user_update_put_schema = {
    "type": "object",
    "properties": {
        "uid": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "full_name": {"type": "string"},
        "role": {"type": "string"}
    },
    "required": ["uid", "email", "full_name", "role"]
}
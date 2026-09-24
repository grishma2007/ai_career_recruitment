def validate_json(data, required_keys):
    """Validate that the incoming JSON has all required keys."""
    if not data:
        return False, "No JSON payload provided."
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return False, f"Missing required keys: {', '.join(missing_keys)}"
    return True, ""

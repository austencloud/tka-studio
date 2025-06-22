"""Shared API constants across desktop and web applications."""

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30

# API Endpoints
ENDPOINTS = {
    "health": "/api/health",
    "sequences": "/api/sequences",
    "settings": "/api/settings",
    "backgrounds": "/api/settings/backgrounds/available",
    "sequence_by_id": "/api/sequences/{id}",
    "save_sequence": "/api/sequences",
    "delete_sequence": "/api/sequences/{id}",
    "export_sequence": "/api/sequences/{id}/export",
    "import_sequence": "/api/sequences/import",
}

# Error messages
ERROR_MESSAGES = {
    "api_unavailable": "API server is not available",
    "sequence_not_found": "Sequence not found",
    "invalid_data": "Invalid data provided",
    "save_failed": "Failed to save sequence",
    "load_failed": "Failed to load sequence",
    "delete_failed": "Failed to delete sequence",
    "export_failed": "Failed to export sequence",
    "import_failed": "Failed to import sequence",
    "network_error": "Network connection error",
    "timeout_error": "Request timeout",
    "server_error": "Internal server error",
    "validation_error": "Data validation error",
}

# Success messages
SUCCESS_MESSAGES = {
    "sequence_saved": "Sequence saved successfully",
    "sequence_loaded": "Sequence loaded successfully",
    "sequence_deleted": "Sequence deleted successfully",
    "sequence_exported": "Sequence exported successfully",
    "sequence_imported": "Sequence imported successfully",
    "settings_saved": "Settings saved successfully",
    "settings_loaded": "Settings loaded successfully",
}

# Settings keys
SETTING_KEYS = {
    "background_type": "ui.background_type",
    "theme": "ui.theme",
    "window_geometry": "ui.window_geometry",
    "last_sequence": "app.last_sequence_id",
    "auto_save": "app.auto_save_enabled",
    "auto_save_interval": "app.auto_save_interval_minutes",
    "default_prop_type": "app.default_prop_type",
    "show_grid": "ui.show_grid",
    "grid_opacity": "ui.grid_opacity",
    "animation_speed": "ui.animation_speed",
}

# Default values
DEFAULT_VALUES = {
    "background_type": "aurora_borealis",
    "theme": "dark",
    "auto_save": True,
    "auto_save_interval": 5,
    "default_prop_type": "staff",
    "show_grid": True,
    "grid_opacity": 0.3,
    "animation_speed": 1.0,
    "sequence_duration": 4.0,
    "beat_duration": 1.0,
}

# HTTP Status codes
HTTP_STATUS = {
    "OK": 200,
    "CREATED": 201,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "INTERNAL_SERVER_ERROR": 500,
    "SERVICE_UNAVAILABLE": 503,
}

# File extensions
FILE_EXTENSIONS = {
    "sequence": ".tka",
    "settings": ".ini",
    "export_json": ".json",
    "export_csv": ".csv",
    "image": ".png",
    "video": ".mp4",
}

# Validation limits
VALIDATION_LIMITS = {
    "max_sequence_name_length": 100,
    "max_sequence_word_length": 50,
    "max_beats_per_sequence": 100,
    "min_beat_duration": 0.1,
    "max_beat_duration": 10.0,
    "max_turns": 10.0,
    "min_turns": -10.0,
}

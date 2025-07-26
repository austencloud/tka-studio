# Modern Domain Module

# Export models for easy importing

__all__ = [
    # Re-export everything from models
] + getattr(
    __import__("desktop.modern.domain.models", fromlist=["__all__"]), "__all__", []
)

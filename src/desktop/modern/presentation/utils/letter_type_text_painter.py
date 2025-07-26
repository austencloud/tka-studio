"""
Letter Type Text Painter - Modern Version

Provides colored HTML text for letter types, matching the legacy implementation.
Used for styling section headers in the option picker.
"""


class LetterTypeTextPainter:
    """
    Utility for generating colored HTML text for different motion types.
    
    Directly based on the legacy letter_type_text_painter.py for consistency.
    """
    
    COLORS = {
        "Shift": "#6F2DA8",
        "Dual": "#00b3ff", 
        "Dash": "#26e600",
        "Cross": "#26e600",
        "Static": "#eb7d00",
        "-": "#000000",
    }

    @classmethod
    def get_colored_text(cls, text: str, bold: bool = False) -> str:
        """
        Generate colored HTML text for the given text.
        
        Args:
            text: The text to colorize (e.g., "Dual-Shift")
            bold: Whether to apply bold styling
            
        Returns:
            HTML string with colored spans
        """
        type_words = text.split("-")
        styled_words = [
            (
                f"<span style='color: {cls.COLORS.get(word, 'black')};"
                f"{' font-weight: bold;' if bold else ''}'>{word}</span>"
            )
            for word in type_words
        ]
        if "-" in text:
            return "-".join(styled_words)
        return "".join(styled_words)

"""
Music Player Service

Service for audio playback functionality using pygame.
Provides play, pause, stop, and seek capabilities.
"""

from __future__ import annotations

import logging
from pathlib import Path

from desktop.modern.core.interfaces.write_services import IMusicPlayerService


logger = logging.getLogger(__name__)

try:
    import pygame

    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    logger.warning("pygame not available - music player functionality will be disabled")


class MusicPlayerService(IMusicPlayerService):
    """
    Music player service using pygame for audio playback.

    Provides basic playback functionality including play, pause, stop,
    and position seeking for music files in acts.
    """

    def __init__(self):
        """Initialize the music player service."""
        self.current_file: Path | None = None
        self.is_initialized = False
        self._position = 0.0
        self._duration = 0.0
        self._playing = False
        self._paused = False

        if PYGAME_AVAILABLE:
            self._initialize_pygame()

        logger.info(
            f"MusicPlayerService initialized (pygame available: {PYGAME_AVAILABLE})"
        )

    def _initialize_pygame(self) -> bool:
        """Initialize pygame mixer."""
        try:
            if not self.is_initialized:
                pygame.mixer.pre_init(
                    frequency=44100, size=-16, channels=2, buffer=2048
                )
                pygame.mixer.init()
                self.is_initialized = True
                logger.info("pygame mixer initialized successfully")
            return True
        except Exception as e:
            logger.exception(f"Failed to initialize pygame mixer: {e}")
            return False

    def load_music(self, file_path: Path) -> bool:
        """
        Load a music file for playback.

        Args:
            file_path: Path to the music file

        Returns:
            True if loaded successfully, False otherwise
        """
        if not PYGAME_AVAILABLE:
            logger.warning("Cannot load music - pygame not available")
            return False

        try:
            if not file_path.exists():
                logger.error(f"Music file does not exist: {file_path}")
                return False

            # Stop any currently playing music
            self.stop()

            # Load the new music file
            pygame.mixer.music.load(str(file_path))
            self.current_file = file_path

            # Try to get duration using pygame.mixer.Sound for certain formats
            try:
                sound = pygame.mixer.Sound(str(file_path))
                self._duration = sound.get_length()
            except Exception:
                # If we can't get duration, set to 0
                self._duration = 0.0
                logger.warning(f"Could not determine duration for {file_path}")

            self._position = 0.0
            self._playing = False
            self._paused = False

            logger.info(
                f"Successfully loaded music: {file_path} (duration: {self._duration:.1f}s)"
            )
            return True

        except Exception as e:
            logger.exception(f"Failed to load music file {file_path}: {e}")
            return False

    def play(self) -> bool:
        """
        Start or resume playback.

        Returns:
            True if playback started, False otherwise
        """
        if not PYGAME_AVAILABLE or not self.current_file:
            return False

        try:
            if self._paused:
                pygame.mixer.music.unpause()
                self._paused = False
            else:
                pygame.mixer.music.play(start=self._position)

            self._playing = True
            logger.debug("Music playback started")
            return True

        except Exception as e:
            logger.exception(f"Failed to start playback: {e}")
            return False

    def pause(self) -> bool:
        """
        Pause playback.

        Returns:
            True if paused successfully, False otherwise
        """
        if not PYGAME_AVAILABLE or not self._playing:
            return False

        try:
            pygame.mixer.music.pause()
            self._playing = False
            self._paused = True
            logger.debug("Music playback paused")
            return True

        except Exception as e:
            logger.exception(f"Failed to pause playback: {e}")
            return False

    def stop(self) -> bool:
        """
        Stop playback and reset position.

        Returns:
            True if stopped successfully, False otherwise
        """
        if not PYGAME_AVAILABLE:
            return False

        try:
            pygame.mixer.music.stop()
            self._playing = False
            self._paused = False
            self._position = 0.0
            logger.debug("Music playback stopped")
            return True

        except Exception as e:
            logger.exception(f"Failed to stop playback: {e}")
            return False

    def set_position(self, position_seconds: float) -> bool:
        """
        Set playback position.

        Note: pygame.mixer.music doesn't support seeking directly,
        so we track position manually and restart from that position.

        Args:
            position_seconds: Position in seconds

        Returns:
            True if position set, False otherwise
        """
        if not PYGAME_AVAILABLE or not self.current_file:
            return False

        try:
            # Clamp position to valid range
            position_seconds = max(0.0, min(position_seconds, self._duration))

            was_playing = self._playing

            # Stop current playback
            self.stop()

            # Set new position
            self._position = position_seconds

            # Resume playback if it was playing before
            if was_playing and position_seconds < self._duration:
                # Note: pygame doesn't support seeking, so we just track position
                # A more advanced implementation would need to use a different audio library
                pygame.mixer.music.play(start=position_seconds)
                self._playing = True

            logger.debug(f"Music position set to {position_seconds:.1f}s")
            return True

        except Exception as e:
            logger.exception(f"Failed to set position to {position_seconds}: {e}")
            return False

    def get_position(self) -> float:
        """
        Get current playback position.

        Returns:
            Current position in seconds
        """
        if not PYGAME_AVAILABLE:
            return 0.0

        # Note: pygame.mixer.music doesn't provide position tracking
        # A more advanced implementation would need to track time manually
        # or use a different audio library

        if pygame.mixer.music.get_busy() and self._playing:
            # Approximate position tracking (not very accurate)
            return self._position

        return self._position

    def get_duration(self) -> float:
        """
        Get total duration of loaded music.

        Returns:
            Duration in seconds, or 0.0 if no music loaded
        """
        return self._duration

    def is_playing(self) -> bool:
        """
        Check if music is currently playing.

        Returns:
            True if playing, False otherwise
        """
        if not PYGAME_AVAILABLE:
            return False

        return self._playing and pygame.mixer.music.get_busy()

    def is_available(self) -> bool:
        """
        Check if music player functionality is available.

        Returns:
            True if pygame is available and initialized
        """
        return PYGAME_AVAILABLE and self.is_initialized

    def get_supported_formats(self) -> list[str]:
        """
        Get list of supported audio formats.

        Returns:
            List of supported file extensions
        """
        if not PYGAME_AVAILABLE:
            return []

        # Common formats supported by pygame
        return [".mp3", ".wav", ".ogg", ".mid", ".midi"]

    def cleanup(self) -> None:
        """Clean up resources."""
        if PYGAME_AVAILABLE and self.is_initialized:
            try:
                self.stop()
                pygame.mixer.quit()
                self.is_initialized = False
                logger.info("Music player cleaned up successfully")
            except Exception as e:
                logger.exception(f"Error during music player cleanup: {e}")

"""
Background Animation Service Interfaces

Interface definitions for background animation services following TKA's clean architecture.
These interfaces support the animated background system with cross-platform compatibility.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IBlobAnimation(ABC):
    """Interface for blob animation operations."""

    @abstractmethod
    def update_blobs(self, delta_time: float) -> None:
        """
        Update blob animations based on time delta.

        Args:
            delta_time: Time elapsed since last update

        Note:
            Web implementation: Uses requestAnimationFrame timing
        """

    @abstractmethod
    def get_blob_positions(self) -> list[dict[str, Any]]:
        """
        Get current blob positions and properties.

        Returns:
            List of blob state dictionaries

        Note:
            Web implementation: Returns data for CSS/WebGL rendering
        """

    @abstractmethod
    def reset_blobs(self) -> None:
        """Reset blobs to initial state."""

    @abstractmethod
    def set_blob_count(self, count: int) -> None:
        """
        Set number of blobs.

        Args:
            count: Number of blobs to maintain

        Note:
            Web implementation: Dynamically creates/removes DOM elements
        """


class ISparkleAnimation(ABC):
    """Interface for sparkle animation operations."""

    @abstractmethod
    def update_sparkles(self, delta_time: float) -> None:
        """
        Update sparkle animations.

        Args:
            delta_time: Time elapsed since last update

        Note:
            Web implementation: Uses CSS animations or WebGL particles
        """

    @abstractmethod
    def add_sparkle(self, position: tuple[float, float]) -> None:
        """
        Add sparkle at position.

        Args:
            position: (x, y) position for sparkle

        Note:
            Web implementation: Creates DOM element or WebGL particle
        """

    @abstractmethod
    def get_sparkle_positions(self) -> list[dict[str, Any]]:
        """
        Get current sparkle positions and properties.

        Returns:
            List of sparkle state dictionaries

        Note:
            Web implementation: Returns data for rendering system
        """

    @abstractmethod
    def clear_sparkles(self) -> None:
        """Clear all sparkles."""


class IWaveEffects(ABC):
    """Interface for wave effect operations."""

    @abstractmethod
    def update_waves(self, delta_time: float) -> None:
        """
        Update wave animations.

        Args:
            delta_time: Time elapsed since last update

        Note:
            Web implementation: Updates CSS transform properties
        """

    @abstractmethod
    def get_wave_parameters(self) -> dict[str, Any]:
        """
        Get current wave parameters.

        Returns:
            Dictionary with wave properties (amplitude, frequency, etc.)

        Note:
            Web implementation: Used for CSS custom properties
        """

    @abstractmethod
    def set_wave_intensity(self, intensity: float) -> None:
        """
        Set wave animation intensity.

        Args:
            intensity: Intensity value (0.0 to 1.0)

        Note:
            Web implementation: Updates CSS animation-duration
        """


class IBubblePhysics(ABC):
    """Interface for bubble physics operations."""

    @abstractmethod
    def update_bubbles(self, delta_time: float) -> None:
        """
        Update bubble physics simulation.

        Args:
            delta_time: Time elapsed since last update

        Note:
            Web implementation: Uses physics engine or manual calculations
        """

    @abstractmethod
    def add_bubble(self, position: tuple[float, float], size: float) -> str:
        """
        Add bubble to simulation.

        Args:
            position: (x, y) starting position
            size: Bubble size

        Returns:
            Unique identifier for the bubble

        Note:
            Web implementation: Creates DOM element with physics properties
        """

    @abstractmethod
    def remove_bubble(self, bubble_id: str) -> bool:
        """
        Remove bubble from simulation.

        Args:
            bubble_id: Unique identifier for bubble

        Returns:
            True if bubble was removed

        Note:
            Web implementation: Removes DOM element
        """

    @abstractmethod
    def get_bubble_positions(self) -> list[dict[str, Any]]:
        """
        Get current bubble positions and properties.

        Returns:
            List of bubble state dictionaries

        Note:
            Web implementation: Returns data for CSS positioning
        """

    @abstractmethod
    def set_gravity(self, gravity: float) -> None:
        """
        Set gravity force for bubbles.

        Args:
            gravity: Gravity force value

        Note:
            Web implementation: Updates physics simulation parameters
        """


class IFishMovement(ABC):
    """Interface for fish movement operations."""

    @abstractmethod
    def update_fish(self, delta_time: float) -> None:
        """
        Update fish movement.

        Args:
            delta_time: Time elapsed since last update

        Note:
            Web implementation: Updates CSS transform for fish sprites
        """

    @abstractmethod
    def get_fish_positions(self) -> list[dict[str, Any]]:
        """
        Get current fish positions and states.

        Returns:
            List of fish state dictionaries

        Note:
            Web implementation: Returns data for sprite positioning
        """

    @abstractmethod
    def set_fish_speed(self, speed: float) -> None:
        """
        Set fish movement speed.

        Args:
            speed: Movement speed multiplier

        Note:
            Web implementation: Updates CSS animation-duration
        """


class IFishSpawning(ABC):
    """Interface for fish spawning operations."""

    @abstractmethod
    def spawn_fish(
        self, fish_type: str, position: tuple[float, float] | None = None
    ) -> str:
        """
        Spawn a new fish.

        Args:
            fish_type: Type of fish to spawn
            position: Optional spawn position (random if None)

        Returns:
            Unique identifier for the spawned fish

        Note:
            Web implementation: Creates DOM element for fish sprite
        """

    @abstractmethod
    def despawn_fish(self, fish_id: str) -> bool:
        """
        Remove fish from simulation.

        Args:
            fish_id: Unique identifier for fish

        Returns:
            True if fish was removed

        Note:
            Web implementation: Removes DOM element
        """

    @abstractmethod
    def get_spawn_rate(self) -> float:
        """
        Get current fish spawn rate.

        Returns:
            Fish spawning rate (fish per second)
        """

    @abstractmethod
    def set_spawn_rate(self, rate: float) -> None:
        """
        Set fish spawn rate.

        Args:
            rate: Fish spawning rate (fish per second)

        Note:
            Web implementation: Updates spawn timer interval
        """


class ISnowflakePhysics(ABC):
    """Interface for snowflake physics operations."""

    @abstractmethod
    def update_snowflakes(self, delta_time: float) -> None:
        """
        Update snowflake physics.

        Args:
            delta_time: Time elapsed since last update

        Note:
            Web implementation: Updates CSS transforms for snowflakes
        """

    @abstractmethod
    def add_snowflake(self, position: tuple[float, float] | None = None) -> str:
        """
        Add snowflake to simulation.

        Args:
            position: Optional starting position (random if None)

        Returns:
            Unique identifier for snowflake

        Note:
            Web implementation: Creates DOM element with physics
        """

    @abstractmethod
    def get_snowflake_positions(self) -> list[dict[str, Any]]:
        """
        Get current snowflake positions.

        Returns:
            List of snowflake state dictionaries

        Note:
            Web implementation: Returns data for DOM positioning
        """

    @abstractmethod
    def set_wind_force(self, force: tuple[float, float]) -> None:
        """
        Set wind force affecting snowflakes.

        Args:
            force: (x, y) wind force vector

        Note:
            Web implementation: Updates physics simulation
        """


class ISantaMovement(ABC):
    """Interface for Santa movement operations."""

    @abstractmethod
    def update_santa_position(self, delta_time: float) -> None:
        """
        Update Santa's position.

        Args:
            delta_time: Time elapsed since last update

        Note:
            Web implementation: Updates CSS transform for Santa sprite
        """

    @abstractmethod
    def get_santa_position(self) -> dict[str, Any]:
        """
        Get Santa's current position and state.

        Returns:
            Santa state dictionary

        Note:
            Web implementation: Returns position data for CSS positioning
        """

    @abstractmethod
    def set_santa_path(self, waypoints: list[tuple[float, float]]) -> None:
        """
        Set Santa's movement path.

        Args:
            waypoints: List of (x, y) waypoints for path

        Note:
            Web implementation: Defines CSS animation keyframes
        """

    @abstractmethod
    def reset_santa_position(self) -> None:
        """Reset Santa to starting position."""


class IShootingStar(ABC):
    """Interface for shooting star operations."""

    @abstractmethod
    def update_shooting_stars(self, delta_time: float) -> None:
        """
        Update shooting star animations.

        Args:
            delta_time: Time elapsed since last update

        Note:
            Web implementation: Updates CSS transform and opacity
        """

    @abstractmethod
    def trigger_shooting_star(self) -> str:
        """
        Trigger a new shooting star.

        Returns:
            Unique identifier for the shooting star

        Note:
            Web implementation: Creates DOM element with animation
        """

    @abstractmethod
    def get_shooting_star_positions(self) -> list[dict[str, Any]]:
        """
        Get current shooting star positions.

        Returns:
            List of shooting star state dictionaries

        Note:
            Web implementation: Returns data for CSS positioning
        """


class IStarTwinkling(ABC):
    """Interface for star twinkling operations."""

    @abstractmethod
    def update_twinkling(self, delta_time: float) -> None:
        """
        Update star twinkling animations.

        Args:
            delta_time: Time elapsed since last update

        Note:
            Web implementation: Updates CSS opacity animations
        """

    @abstractmethod
    def get_star_states(self) -> list[dict[str, Any]]:
        """
        Get current star twinkling states.

        Returns:
            List of star state dictionaries

        Note:
            Web implementation: Returns opacity and brightness data
        """

    @abstractmethod
    def set_twinkle_rate(self, rate: float) -> None:
        """
        Set star twinkling rate.

        Args:
            rate: Twinkling frequency

        Note:
            Web implementation: Updates CSS animation timing
        """


class ICometTrajectory(ABC):
    """Interface for comet trajectory operations."""

    @abstractmethod
    def update_comet(self, delta_time: float) -> None:
        """
        Update comet position and trail.

        Args:
            delta_time: Time elapsed since last update

        Note:
            Web implementation: Updates CSS transform and SVG path
        """

    @abstractmethod
    def get_comet_position(self) -> dict[str, Any]:
        """
        Get current comet position and properties.

        Returns:
            Comet state dictionary

        Note:
            Web implementation: Returns position for CSS positioning
        """

    @abstractmethod
    def reset_comet(self) -> None:
        """Reset comet to starting position."""

    @abstractmethod
    def set_comet_speed(self, speed: float) -> None:
        """
        Set comet movement speed.

        Args:
            speed: Movement speed multiplier

        Note:
            Web implementation: Updates CSS animation-duration
        """


class IMoonPositioning(ABC):
    """Interface for moon positioning operations."""

    @abstractmethod
    def update_moon_position(self, delta_time: float) -> None:
        """
        Update moon position.

        Args:
            delta_time: Time elapsed since last update

        Note:
            Web implementation: Updates CSS transform for moon
        """

    @abstractmethod
    def get_moon_position(self) -> dict[str, Any]:
        """
        Get current moon position.

        Returns:
            Moon state dictionary

        Note:
            Web implementation: Returns position data for CSS
        """

    @abstractmethod
    def set_moon_phase(self, phase: float) -> None:
        """
        Set moon phase.

        Args:
            phase: Moon phase (0.0 to 1.0)

        Note:
            Web implementation: Updates CSS mask or clip-path
        """


class IUfoBehavior(ABC):
    """Interface for UFO behavior operations."""

    @abstractmethod
    def update_ufo(self, delta_time: float) -> None:
        """
        Update UFO behavior and position.

        Args:
            delta_time: Time elapsed since last update

        Note:
            Web implementation: Updates CSS transform and effects
        """

    @abstractmethod
    def get_ufo_position(self) -> dict[str, Any]:
        """
        Get current UFO position and state.

        Returns:
            UFO state dictionary

        Note:
            Web implementation: Returns position data for CSS
        """

    @abstractmethod
    def trigger_ufo_event(self, event_type: str) -> None:
        """
        Trigger UFO special event.

        Args:
            event_type: Type of event to trigger

        Note:
            Web implementation: Triggers CSS animations or effects
        """

    @abstractmethod
    def set_ufo_behavior_mode(self, mode: str) -> None:
        """
        Set UFO behavior mode.

        Args:
            mode: Behavior mode ('patrol', 'chase', 'idle', etc.)

        Note:
            Web implementation: Changes CSS animation sets
        """

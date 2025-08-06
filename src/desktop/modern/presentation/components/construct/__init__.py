"""
Components module for construct tab layout management.

This module contains specialized components that handle specific aspects
of the construct tab layout:

- PanelFactory: Creates individual UI panels
- TransitionAnimator: Manages smooth transitions between panels
- ComponentConnector: Handles inter-component communication
"""

from __future__ import annotations

from .component_connector import ComponentConnector
from .panel_factory import PanelFactory
from .transition_animator import TransitionAnimator


__all__ = [
    "ComponentConnector",
    "PanelFactory",
    "TransitionAnimator",
]

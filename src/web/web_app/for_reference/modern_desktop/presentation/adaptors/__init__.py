"""
Qt Adaptors for Framework-Agnostic Services

This module contains Qt adaptors that bridge between framework-agnostic services
and Qt UI components. Adaptors convert service callbacks to Qt signals and
delegate method calls to the underlying services.
"""

from __future__ import annotations

from .sequence_card_display_adaptor import SequenceCardDisplayAdaptor


__all__ = [
    "SequenceCardDisplayAdaptor",
]

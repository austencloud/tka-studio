from __future__ import annotations
from main_window.main_widget.main_background_widget.backgrounds.snowfall.new.snowflake import (
    Snowflake,
)
from PyQt6.QtCore import QRunnable


class SnowflakeUpdateTask(QRunnable):
    def __init__(self, snowflakes: list[Snowflake]):
        super().__init__()
        self.snowflakes = snowflakes

    def run(self):
        for snowflake in self.snowflakes:
            snowflake.update_position()

from __future__ import annotations


class ThumbnailBoxState:
    def __init__(self, thumbnails: list[str | None] | None = None):
        self.thumbnails: list[str] = (
            [t for t in thumbnails if t is not None] if thumbnails else []
        )
        self.current_index: int = 0

    def update_thumbnails(self, thumbnails: list[str]):
        self.thumbnails = thumbnails
        if self.current_index >= len(self.thumbnails):
            self.current_index = max(0, len(self.thumbnails) - 1)

    def set_current_index(self, index: int):
        if 0 <= index < len(self.thumbnails):
            self.current_index = index

    def get_current_thumbnail(self) -> str | None:
        if self.thumbnails and 0 <= self.current_index < len(self.thumbnails):
            return self.thumbnails[self.current_index]
        return None

    def clear(self):
        self.thumbnails.clear()
        self.current_index = 0

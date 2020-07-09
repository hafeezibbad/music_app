from typing import Optional


class SongsServiceError(RuntimeError):
    def __init__(self, message: Optional[str] = None):
        self.message = message

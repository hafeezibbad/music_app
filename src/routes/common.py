from typing import Optional

from flask import Request

from src.music_app.manager import MusicAppManager


def create_music_app_manager(
        incoming_request: Optional[Request] = None,
        items_per_page: Optional[int] = 20
) -> MusicAppManager:
    return MusicAppManager(requester_ip=incoming_request.remote_addr, items_per_page=items_per_page)

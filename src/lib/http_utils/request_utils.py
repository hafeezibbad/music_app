from typing import Optional, Dict, Any
from requests import Session
from typing_extensions import Literal


def handle_api_request(
        method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
        url: str = '',
        headers: Optional[dict] = None,
        body: Optional[dict] = None,
        session: Session = Session(),
        params: Optional[Dict[str, Any]] = None
):
    assert url, "No URL specified to make the request"
    headers = headers or dict()

    r = session.request(method, url, json=body, headers=headers, params=params)

    return {"statusCode": r.status_code, "body": r.text, "headers": r.headers}

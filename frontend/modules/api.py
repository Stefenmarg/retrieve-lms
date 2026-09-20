import httpx
from modules.config import settings
from nicegui import app

BASE_URL = settings.app_address
TIMEOUT = settings.timeout_time_httpx_seconds

# All API requests to the backend are done from here where we
# make a new httpx.Client per call and per user. I tried using
# one module-level client but since NiceGUI is a multiuser server
# process it allowed sharing a client's cookie jar to be shared state
# across every other user's session. That caused one user's refresh_token
# leaking into another user's request which is a huge security risk.
# Current implementation allows passing of refresh_token explicitly
# from app.storage.user to the request.


def _request(method: str, endpoint: str, json: dict | None):
    # Get the refresh token and attach it to the cookies sent by
    # httpx at every request
    refresh_token = app.storage.user.get("refresh_token")
    cookies = {"refresh_token": refresh_token} if refresh_token else {}

    # Make a call at that endpoint with the request type,
    # the parameters, the json data if any as well as the
    # authorization "Bearer: " auth header
    with httpx.Client(base_url=BASE_URL, timeout=TIMEOUT) as http_client:
        response = http_client.request(
            method=method.upper(),
            url=f"/api/v1{endpoint}",
            json=json,
            headers=_auth_header(),
            cookies=cookies,
        )

    # In debug mode enable showing the status code and the exact reply of the endpoint
    if settings.app_debug:
        print("_request: ", response.status_code, response.text)

    # If the endpoint sends back a refresh token, save it
    _store_refresh_token(response)

    return response


def _store_refresh_token(response: httpx.Response):
    # Get the refresh token from the cookie and if it exists
    # save it to the secure storage
    new_refresh_token = response.cookies.get("refresh_token")
    if new_refresh_token:
        app.storage.user["refresh_token"] = new_refresh_token


# This function makes requests to the backend and if it gets "401 Unauthorized"
# it tries to refresh the token and retries the request and if it still
# fail with "401 Unauthorized" it clears the storage
def _make_api_call(method: str, endpoint: str, json: dict | None = None):
    response = _request(method, endpoint, json)

    if response.status_code == 401:
        if _refresh_access_token():
            # retry once with the new access token
            response = _request(method, endpoint, json)
        else:
            # refresh failed thus user must log in again
            _clear_session()

    return response


# Creates the Authorization Bearer header used in _request
def _auth_header() -> dict:
    token = app.storage.user.get("access_token")
    return {"Authorization": f"Bearer {token}"} if token else {}


# Makes a request at /api/v1/auth/refresh using this user's own
# stored refresh token and returns True if a new access token was obtained
def _refresh_access_token() -> bool:

    response = _request("POST", "/auth/refresh", None)

    if settings.app_debug:
        print("refresh: ", response.status_code, response.text)

    if response.status_code != 200:
        return False

    app.storage.user["access_token"] = response.json()["token"]

    return True


def _clear_session():
    app.storage.user.pop("access_token", None)
    app.storage.user.pop("refresh_token", None)


def register(full_name: str, email: str, password: str, role: str):
    return _make_api_call(
        "POST",
        "/auth/register",
        {
            "full_name": full_name,
            "email": email,
            "password": password,
            "role": role,
        },
    )


def login(email: str, password: str):
    response = _make_api_call(
        "POST",
        "/auth/login",
        {
            "email": email,
            "password": password,
        },
    )

    if response.status_code == 200:
        app.storage.user["access_token"] = response.json()["token"]

    return response


def logout():
    # server-side: revokes tokens + clear cookie in the jar
    response = _make_api_call("POST", "/auth/logout")
    _clear_session()
    return response


def get_status():
    return _make_api_call("GET", "/auth/status")

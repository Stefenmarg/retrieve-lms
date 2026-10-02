from modules.api import clear_session, make_api_call
from nicegui import app


def register(full_name: str, email: str, password: str, role: str):
    return make_api_call(
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
    response = make_api_call(
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
    response = make_api_call("POST", "/auth/logout")
    clear_session()
    return response


def get_status():
    return make_api_call("GET", "/auth/status")

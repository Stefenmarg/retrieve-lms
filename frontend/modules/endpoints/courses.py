from modules.api import clear_session, make_api_call
from nicegui import app


def list_available():
    response = make_api_call("GET", "/courses/list/available")
    if response.status_code != 200:
        return None
    return response.json()


def list_joined():
    response = make_api_call("GET", "/courses/list")
    if response.status_code != 200:
        return None
    return response.json()


def join_course_by_id(course_id: int, message: str | None = None):
    response = make_api_call(
        "POST",
        "/courses/join",
        {
            "course_id": course_id,
            "message": message if message else "No message was provided",
        },
    )
    if response.status_code != 200:
        return None
    return response.json()

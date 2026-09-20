import functools
from urllib.parse import quote

from modules.api import get_status
from nicegui import ui


# This is a decorator that gets used when defining a protected route.
# It checks the current authentication status of user and if the user
# is not authenticated it sends them to the /auth page to login
# or register.
#   It also provides the auth page with information
# about the redirection (what page they were originally trying to access)
# so when they log-in or register they get sent back to
# the page they where trying to access
def needs_authentication(path: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            response = get_status()
            if response.status_code != 200:
                redirected_to = quote(path, safe="")
                ui.navigate.to(f"/auth?redirected=true&redirected_to={redirected_to}")
                return None
            return func(*args, **kwargs)

        return wrapper

    return decorator

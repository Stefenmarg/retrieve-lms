import modules.api as api
from modules.form_rules import email_validation_rules
from nicegui import ui


def login_page(slot, redirected, redirected_to):
    def try_login():
        # Validate form content
        fields_valid = [email.validate()]
        if not all(fields_valid):
            return

        # Send login request
        response = api.login(
            email.value,
            password.value,
        )

        # If login fails, notify the user why it failed using the feedback
        # the backend sent. If not feedback revert to a generic failure message
        if response.status_code != 200:
            try:
                detail = response.json().get("detail", "Login failed")
            except ValueError:
                detail = f"Registration failed ({response.status_code})"

            ui.notify(detail, color="negative")
            return

        ui.notify("Logged in successfully")

        # Navigate to the page the user originally wanted to access
        if redirected:
            ui.navigate.to(redirected_to)
            return

        # Else navigate to the dashboard
        ui.navigate.to("/dashboard")

    with slot:
        ui.label("Login to your account")

        # The login form
        with ui.column().classes("w-full"):
            email = (
                ui.input(placeholder="Your email", validation=email_validation_rules)
                .props("autofocus")
                .on("keydown.enter", lambda: password.run_method("focus"))
                .classes("w-full")
            )

            password = (
                ui.input(
                    placeholder="Enter password",
                    password=True,
                    password_toggle_button=True,
                )
                .on("keydown.enter", try_login)
                .classes("w-full")
            )

        with ui.row().classes("justify-end gap-2 q-mt-lg"):
            ui.button("Login", on_click=try_login).props("color=primary")

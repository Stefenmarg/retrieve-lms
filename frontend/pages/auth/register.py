import modules.api as api
from modules.config import settings
from modules.form_rules import (
    email_validation_rules,
    full_name_validation_rules,
    password_validation_rules,
)
from nicegui import ui


def register_page(slot, redirected, redirected_to):
    # The allowed register roles, if the platform is
    # in demo mode allow admin account creation
    SIGNUP_ROLES = ["student", "teacher"]
    if settings.app_demo:
        SIGNUP_ROLES.append("admin")

    def try_register():
        # Validate form content
        fields_valid = [
            full_name.validate(),
            email.validate(),
            password.validate(),
            verification_password.validate(),
        ]

        if not all(fields_valid):
            return

        if password.value != verification_password.value:
            ui.notify("Passwords do not match", color="negative")
            return

        # Send registration request
        response = api.register(
            full_name.value, email.value, password.value, role.value
        )

        # If account was not created, notify the user why it failed using the feedback
        # the backend backend sent. If not feedback revert to a generic failure message
        if response.status_code != 201:
            try:
                detail = response.json().get("detail", "Registration failed")
            except ValueError:
                detail = f"Registration failed ({response.status_code})"

            ui.notify(detail, color="negative")
            return

        ui.notify("Registered successfully")

        # Now that the account was created, send login request
        response = api.login(
            email.value,
            password.value,
        )
        # If login fails, notify the user why it failed using the feedback
        # the backend sent. If not feedback revert to a generic failure message
        if response.status_code != 200:
            try:
                detail = response.json().get("detail", "Registration failed")
            except ValueError:
                detail = f"Registration failed ({response.status_code})"

            ui.notify(detail, color="negative")
            return

        # Navigate to the page the user originally wanted to access
        if redirected:
            ui.navigate.to(redirected_to)
            return

        # Else navigate to the dashboard
        ui.navigate.to("/dashboard")

    with slot:
        ui.label("Create an account")

        # The register form
        with ui.column().classes("w-full"):
            full_name = (
                ui.input(
                    placeholder="Your full name", validation=full_name_validation_rules
                )
                .props("autofocus")
                .on("keydown.enter", lambda: email.run_method("focus"))
                .classes("w-full")
            )

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
                    validation=password_validation_rules,
                )
                .on("keydown.enter", lambda: verification_password.run_method("focus"))
                .classes("w-full")
            )

            verification_password = (
                ui.input(
                    placeholder="Re-Enter password",
                    password=True,
                    password_toggle_button=True,
                    validation=password_validation_rules,
                )
                .on("keydown.enter", try_register)
                .classes("w-full")
            )

        with ui.row().classes("justify-center gap-2 q-mt-lg"):
            role = ui.toggle(
                SIGNUP_ROLES,
                value=SIGNUP_ROLES[0],
            )

        with ui.row().classes("justify-end gap-2 q-mt-lg"):
            ui.button("Register", on_click=try_register).props("color=primary")

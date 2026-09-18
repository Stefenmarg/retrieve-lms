from modules.validity_rules import (
    email_validation_rules,
    full_name_validation_rules,
    password_validation_rules,
)
from nicegui import ui


def register_page(slot, redirected, redirected_to):
    def try_register():
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

        ui.notify("Registered successfully")

        if redirected:
            ui.navigate.to(redirected_to)
            return

        ui.navigate.to("/dashboard")

    with slot:
        ui.label("Create an account")

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

        with ui.row().classes("justify-end gap-2 q-mt-lg"):
            ui.button("Register", on_click=try_register).props("color=primary")

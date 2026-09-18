from modules.validity_rules import email_validation_rules, password_validation_rules
from nicegui import ui


def login_page(slot, redirected, redirected_to):
    def try_login():
        fields_valid = [password.validate(), email.validate()]
        if not all(fields_valid):
            return

        ui.notify("Logged in successfully")

        if redirected:
            ui.navigate.to(redirected_to)
            return

        ui.navigate.to("/dashboard")

    with slot:
        ui.label("Login to your account")

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
                    validation=password_validation_rules,
                )
                .on("keydown.enter", lambda: try_login)
                .classes("w-full")
            )

        with ui.row().classes("justify-end gap-2 q-mt-lg"):
            ui.button("Login", on_click=try_login).props("color=primary")

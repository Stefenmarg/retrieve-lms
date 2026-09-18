from functools import partial

from modules.config import settings
from nicegui import ui
from pages.auth.login import login_page
from pages.auth.register import register_page


def auth_page(drawer_slot, main_slot, redirected=False, redirected_to="/"):
    ui.page_title("Retrieve - Auth")

    drawer_slot.clear()
    with drawer_slot:
        ui.separator()
        ui.label("Auth label")

    main_slot.clear()
    with main_slot:
        with ui.element("div").classes(
            "fixed inset-0 flex items-center justify-center bg-black/50 z-50"
        ):
            # The actual modal box
            with ui.card().classes("w-96 items-center p-6"):
                if redirected:
                    ui.label(
                        "The page you are trying to access requires authentication. Please login to continue"
                    ).classes("text-xl font-large")
                with ui.tabs().classes("w-full") as tabs:
                    one = ui.tab("Login")
                    two = ui.tab("Register")

                with ui.tab_panels(tabs, value=one).classes("w-full"):
                    with ui.tab_panel(one).classes(
                        "flex flex-col items-center"
                    ) as login_slot:
                        login_page(login_slot, redirected, redirected_to)

                    with ui.tab_panel(two).classes(
                        "flex flex-col items-center"
                    ) as register_slot:
                        register_page(register_slot, redirected, redirected_to)

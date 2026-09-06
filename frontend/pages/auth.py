from modules.config import settings
from nicegui import ui


def auth_page(drawer_slot, main_slot):
    ui.page_title("Retrieve - Auth")

    drawer_slot.clear()
    with drawer_slot:
        ui.separator()
        ui.label("Auth label")

    main_slot.clear()
    with main_slot:
        ui.label("Auth to be welcomed to home")

        with ui.element("div").classes(
            "fixed inset-0 flex items-center justify-center bg-black/50 z-50"
        ):
            # The actual modal box
            with ui.card().classes("w-96 items-center p-6"):
                with ui.tabs().classes("w-full") as tabs:
                    one = ui.tab("Sign-in")
                    two = ui.tab("Sign-up")

                with ui.tab_panels(tabs, value=two).classes("w-full"):
                    with ui.tab_panel(one).classes("flex flex-col items-center"):
                        ui.label("First tab")
                    with ui.tab_panel(two).classes("flex flex-col items-center"):
                        ui.label("Second tab")

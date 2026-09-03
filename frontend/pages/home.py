from modules.config import settings
from nicegui import ui


def main_page(drawer_slot, main_slot):
    ui.page_title("Retrieve - Home")

    drawer_slot.clear()
    with drawer_slot:
        ui.separator()
        ui.label("Home label")

    main_slot.clear()
    with main_slot:
        ui.label("Welcome home")

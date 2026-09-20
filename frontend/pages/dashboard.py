from functools import partial

from modules.config import settings
from modules.security import needs_authentication
from nicegui import ui
from pages.auth.login import login_page
from pages.auth.register import register_page


@needs_authentication("/dashboard")
def dashboard_page(drawer_slot, main_slot):
    ui.page_title("Retrieve - Dashboard")

    drawer_slot.clear()

    main_slot.clear()
    with main_slot:
        ui.label("Dashboard protected view")

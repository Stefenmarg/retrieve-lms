from functools import partial

from modules.api import get_token_payload
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
        ui.label(f"Welcome, {get_token_payload()['full_name']}!")

        columns = [
            {
                "name": "name",
                "label": "Name",
                "field": "name",
                "required": True,
                "align": "left",
            },
            {"name": "age", "label": "Age", "field": "age", "sortable": True},
        ]
        rows = [
            {"name": "Alice", "age": 18},
            {"name": "Bob", "age": 21},
            {"name": "Carol"},
        ]

        with ui.row(wrap=True):
            with ui.column():
                ui.label("Joined Courses")
                ui.table(columns=columns, rows=rows, row_key="name")
            ui.space()
            with ui.column():
                ui.label("Notifications")
                ui.table(columns=columns, rows=rows, row_key="name")

from modules.api import get_token_payload
from modules.endpoints.courses import list_available, list_joined
from modules.security import needs_authentication
from nicegui import ui
from pages.dashboard.available_courses import available_courses
from pages.dashboard.joined_courses import joined_courses

course_columns = [
    {"name": "name", "label": "Course name", "field": "name", "sortable": True},
    {
        "name": "description",
        "label": "Course description",
        "field": "description",
        "sortable": False,
    },
    {
        "name": "restriction_status",
        "label": "Join type",
        "field": "restriction_status",
        "sortable": False,
    },
]


@needs_authentication("/dashboard")
def dashboard_page(drawer_slot, main_slot):
    ui.page_title("Retrieve - Dashboard")

    drawer_slot.clear()

    main_slot.clear()

    with main_slot:
        ui.label(f"Welcome, {get_token_payload()['full_name']}!")

        joined_courses(main_slot, course_columns)

        available_courses(main_slot, course_columns)

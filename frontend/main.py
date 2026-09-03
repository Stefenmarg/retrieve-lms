from functools import partial

from modules.config import settings
from nicegui import ui
from pages.home import main_page


def root():
    with (
        ui.header(elevated=True)
        .classes("items-center justify-between")
        .style("background-color: #2E2F2F")
    ):
        ui.label(f"{settings.app_name}")
        ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props(
            "flat color=#2E2F2F"
        )

    with ui.left_drawer(fixed=False, top_corner=True, bottom_corner=True).style(
        "background-color: #E5E5E5"
    ) as left_drawer:
        ui.label("Navigation menu")
        ui.separator()
        # Static navigation menu
        ui.link("Home", "/")

        # Dynamic navigation menu set by the child page
        drawer_slot = ui.column()

    # Slot where content is set by child page
    main_slot = ui.column()

    # URL Based routing for page access
    ui.sub_pages(
        {
            "/": partial(main_page, drawer_slot, main_slot),
        },
        show_404=False,
    )

    with ui.footer().style("background-color: #2E2F2F"):
        with ui.row().classes("w-full justify-center gap-20"):
            with ui.column():
                ui.label("Information").classes("text-xl font-medium")
                ui.separator()
                ui.link("Codeberg Repo", "https://codeberg.org/stefenmarg/retrieve-lms")
            with ui.column():
                ui.label("Documentation").classes("text-xl font-medium")
                ui.separator()
                ui.link("NiceGUI", "https://nicegui.io/")


ui.run(root, host="0.0.0.0", port=8001)

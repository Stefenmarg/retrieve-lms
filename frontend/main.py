from functools import partial

from modules.config import settings
from nicegui import app, ui
from pages.auth.auth import auth_page
from pages.home import main_page


def root():
    with (
        ui.header(elevated=True)
        .classes("items-center justify-between")
        .style("background-color: #2E2F2F")
    ):
        ui.label(f"{settings.app_name}")
        ui.button(on_click=lambda: left_drawer.toggle(), icon="menu")

    with ui.left_drawer(
        fixed=False, top_corner=True, bottom_corner=True
    ) as left_drawer:
        ui.label("Navigation menu")
        ui.separator()

        # Navigation menu set by the root page
        ui.link("Home", "/")

        # Dynamic navigation menu set by the child page
        drawer_slot = ui.column()

        # The continuation of navigation menu set by the root page
        ui.separator()
        ui.label("Important links")

        ui.link("GitLab Repo", "https://gitlab.com/stefenmarg/retrieve-lms")
        ui.link("GitHub Mirror", "https://github.com/Stefenmarg/retrieve-lms")
        ui.link("NiceGUI", "https://nicegui.io/")
        ui.link(
            "Material Icons", "https://fonts.google.com/icons?icon.set=Material+Icons"
        )

    # Slot where content is set by child page
    main_slot = ui.column()

    # URL Based routing for page access
    ui.sub_pages(
        {
            "/": partial(main_page, drawer_slot, main_slot),
            "/auth": partial(auth_page, drawer_slot, main_slot),
        },
        show_404=False,
    )

    with ui.footer().style("background-color: #2E2F2F"):
        with ui.row().classes("w-full justify-center gap-20"):
            ui.label("This platform is still in the Alpha phase.").classes(
                "text-xl font-large"
            )


app.add_static_files("/static", "static")

ui.run(
    root,
    host="0.0.0.0",
    port=8001,
    favicon=f"{settings.app_address}/static/favicons/favicon-32x32.png",
    reload=True,
)

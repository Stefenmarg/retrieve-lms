from modules.config import settings
from nicegui import ui

carousel_images = [
    {"url": "https://placehold.co/600x400", "width": "600"},
    {"url": "https://placehold.co/600x400", "width": "600"},
    {"url": "https://placehold.co/600x400", "width": "600"},
]


def main_page(drawer_slot, main_slot):
    ui.page_title("Retrieve - Home")

    drawer_slot.clear()
    with drawer_slot:
        ui.separator()
        ui.label("Home label")

    main_slot.clear()
    with main_slot:
        ui.label("Welcome home")

        with ui.element("div").classes(
            "fixed inset-0 flex items-center justify-center bg-black/50 z-50"
        ):
            with ui.carousel(animated=True, arrows=True, navigation=True).props(
                "height=400px"
            ) as carousel:
                for image in carousel_images:
                    with ui.carousel_slide().classes("p-0"):
                        ui.image(f"{image['url']}").classes(f"w-[{image['width']}px]")

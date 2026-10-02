from shlex import join

from modules.endpoints.courses import join_course_by_id, list_available
from nicegui import ui


def join_course(course: dict):
    course_type = course["restriction_status"]

    course_closed = course["restriction_status"] == "closed"
    course_request = course["restriction_status"] == "request"
    course_open = course["restriction_status"] == "open"

    if course_closed
        ui.notify("You cannot join closed courses", color="negative")
        return

    with ui.dialog() as dialog, ui.card():
        ui.label(f"Join course '{course['name']}'?")

        message = "None provided"
        if course_request:
            join_message = ui.textarea(
                label="Your request reason",
                placeholder="Your message",
            )
            message=join_message.value

        with ui.row():
            ui.button(
                "Join",
                on_click=lambda: (
                    join_course_by_id(
                        int(
                            course["id"],
                        ),
                        message=message
                    ),
                    dialog.close(),
                ),
            )

            ui.button("Cancel", on_click=dialog.close).props("flat")
    dialog.open()


def available_courses(slot, course_columns, pagination_size: int = 5):
    with slot:
        courses = list_available()

        ui.label("Courses available to join").classes("text-xl mt-2")

        table = ui.table(
            columns=course_columns,
            rows=courses,
            row_key="name",
            pagination=pagination_size,
        )

        table.add_slot(
            "body-cell-name",
            """
            <q-td :props="props">
                <q-btn flat :label="props.value"
                       @click="() => $parent.$emit('join', props.row)" />
            </q-td>
            """,
        )

        table.on("join", lambda e: join_course(e.args))

        table.add_slot(
            "body-cell-restriction_status",
            """
            <q-td :props="props">
                <q-badge :color="props.value === 'closed' ? 'red' : props.value === 'open' ? 'green' : 'blue'">
                    {{ props.value.toUpperCase() }}
                </q-badge>
            </q-td>
            """,
        )

from modules.endpoints.courses import list_joined
from nicegui import ui


def joined_courses(slot, course_columns, pagination_size: int = 5):
    with slot:
        courses = list_joined()

        ui.label("Courses you have joined").classes("text-xl mt-2")

        table = ui.table(
            columns=course_columns,
            rows=courses,
            row_key="name",
            pagination=pagination_size,
        )

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

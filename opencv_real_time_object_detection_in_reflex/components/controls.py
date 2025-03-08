
import reflex as rx
from opencv_real_time_object_detection_in_reflex.states.camera_state import CameraState

def controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.cond(
                    CameraState.camera_active,
                    "Stop Camera",
                    "Start Camera"
                ),
                on_click=CameraState.toggle_camera,
                class_name=rx.cond(
                    CameraState.camera_active,
                    "bg-red-500 hover:bg-red-600",
                    "bg-green-500 hover:bg-green-600"
                ) + " text-white px-6 py-2 rounded-lg transition-colors duration-200 font-medium"
            ),
            class_name="flex space-x-4"
        ),
        rx.el.div(
            rx.el.p(
                "FPS: ",
                CameraState.fps,
                class_name="text-sm text-gray-600"
            ),
            class_name="mt-4"
        ),
        class_name="p-4 bg-white rounded-lg shadow-md space-y-4"
    )


# import imgui
# from imgui.integrations.glfw import GlfwRenderer

import scintillator_display.compat.imgui as imgui
from scintillator_display.compat.imgui.integrations.glfw import GlfwRenderer


import scintillator_display.display.impl_a.graphics as graphics


def ui_spacing():
    """
    Creates a blank space in the user interface
    """

    for _ in range(5):
        imgui.spacing()


def ui_section(section_name, top_margin=True):
    """
    Decorator constructor to wrap a user interface
    section with a title: reduce the repetition
    of creating a separation for every section
    """

    # constructed decorator
    def decorator(func):
        # wrap the method, building the title
        # of the section first, before drawing
        # the rest of the section

        def wrapper(*args, **kwargs):
            if top_margin:
                ui_spacing()

            # display section title
            imgui.text(section_name)
            imgui.separator()

            # draw the rest of the section
            func(*args, **kwargs)

        return wrapper

    return decorator


class ParameterInterface:
    def __init__(
        self,
        window,
    ):
        """
        Parameter Interface: Manages the state of the parameters
        controlled by the user, and draws the interface

        :param window: glfw window
        :param on_evaluate: Callback for a new user function's evaluation call
        :param on_change_ball_color: Callback to change ball color
        :param on_change_surface_color: Callback to change surface color
        """

        # create DearImGui instance for ui drawing
        imgui.create_context()

        # create bindings to Glfw rendering backend
        # the application manages its own callbacks
        self._imgui_impl = GlfwRenderer(window, attach_callbacks=False)



        # camera data
        self.camera = graphics.orbit_controls.CameraOrbitControls()

        self.light_color = [1.0, 1.0, 1.0]
        self.background_color = [0.86, 0.87, 0.87]

        self.ambient_strength = 0.2
        self.diffuse_strength = 0.2
        self.diffuse_base = 0.3
        self.specular_strength = 0.1
        self.specular_reflection = 16.0


    @property
    def want_keyboard(self):
        return imgui.get_io().want_capture_keyboard

    @property
    def want_mouse(self):
        return imgui.get_io().want_capture_mouse

    @property
    def impl(self):
        return self._imgui_impl
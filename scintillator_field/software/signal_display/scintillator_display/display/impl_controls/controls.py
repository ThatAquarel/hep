import scintillator_display.compat.glfw as glfw
import scintillator_display.compat.imgui as imgui

from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT


class Controls:
    def __init__(self):
        self.window = glfw.create_window(None, None, None, None, None)
        glfw.set_window_size_callback(self.window, self.window_size_callback)

        self.width, self.height = 0, 0

    def window_size_callback(self, window, width, height):
        self.width, self.height = width, height

    def on_render(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        imgui.set_next_window_position(0, 0, condition=imgui.ONCE)
        imgui.set_next_window_size(self.width, self.height, condition=imgui.ALWAYS)
        imgui.begin(
            "System Display",
            flags=imgui.WINDOW_NO_RESIZE
            | imgui.WINDOW_NO_MOVE
            | imgui.WINDOW_NO_COLLAPSE,
        )

        imgui.text("dslkfajfdslkajdfklsajklsdfajkldsfjklfd")

        imgui.end()

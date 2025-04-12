import scintillator_display.compat.glfw as glfw
import scintillator_display.compat.imgui as imgui

from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

from .load_res import load_texture, load_font
from scintillator_display.display.impl_a.graphics.parameter_interface import ui_section, ui_spacing

class Controls:
    def __init__(self):
        self.window = glfw.create_window(None, None, None, None, None)
        glfw.set_window_size_callback(self.window, self.window_size_callback)

        self.width, self.height = 0, 0

        # ffmpeg -i sc_bw.png -vf "scale=-1:48" hep_48.png
        self.hep = load_texture("hep_48.png")
        # ffmpeg -i sc_bw.png -vf "scale=-1:64" sc_64.png
        self.sc = load_texture("sc_64.png")

        self.font = load_font("Poppins-Regular.ttf", 24)

    def window_size_callback(self, window, width, height):
        self.width, self.height = width, height

    def on_render(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        imgui.set_next_window_position(0, 0, condition=imgui.ONCE)
        imgui.set_next_window_size(self.width, self.height, condition=imgui.ALWAYS)
        imgui.begin(
            " ",
            flags=imgui.WINDOW_NO_RESIZE
            | imgui.WINDOW_NO_MOVE
            | imgui.WINDOW_NO_COLLAPSE,
        )

        imgui.separator()

        imgui.push_font(self.font)
        imgui.text("The Scintillating Chamber")
        imgui.pop_font()

        imgui.separator()

        imgui.image(*self.hep)
        imgui.same_line()
        imgui.image(*self.sc)

        imgui.separator()

        imgui.end()

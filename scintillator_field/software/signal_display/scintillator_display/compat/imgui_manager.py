import imgui
from imgui.integrations.glfw import GlfwRenderer

class ImguiManager:
    def __init__(self, window):
        imgui.create_context()
        self._impl: GlfwRenderer = GlfwRenderer(window, attach_callbacks=False)

    @property
    def impl(self) -> GlfwRenderer:
        return self._impl
    
    @property
    def want_keyboard(self):
        return imgui.get_io().want_capture_keyboard    

    @property
    def want_mouse(self):
        return imgui.get_io().want_capture_mouse

    def refresh_font_texture(self):
        self._impl.refresh_font_texture()

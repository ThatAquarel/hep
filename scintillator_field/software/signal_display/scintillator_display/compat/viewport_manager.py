import glfw
import imgui

from scintillator_display.compat.imgui_manager import ImguiManager

class ViewportManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ViewportManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.width, self.height = (1280, 720)
        self.window = self.create_window((self.width, self.height), "Scintillating Chamber")

        self.viewports: list[Viewport] = []
        self.vp_count = 0
        self._current_vp = 0

        self.imgui = ImguiManager(self.window)

    def render_loop(self):
        while not glfw.window_should_close(self.window):
            for vp in self.viewports:
                vp.on_render()

            imgui.render()
            self.imgui.impl.process_inputs()
            self.imgui.impl.render(imgui.get_draw_data())

            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()

    def create_window(self, window_size, name):
        # throw exception if glfw failed to init
        if not glfw.init():
            raise Exception("GLFW could not be initialized.")

        # enable multisampling (antialiasing) on glfw window
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # create window and context
        window = glfw.create_window(*window_size, name, None, None)
        if not window:
            glfw.terminate()
            raise Exception("GLFW window could not be created.")
        glfw.make_context_current(window)

        glfw.set_cursor_pos_callback(window, self._cursor_pos_callback)
        glfw.set_mouse_button_callback(window, self._mouse_button_callback)
        glfw.set_scroll_callback(window, self._scroll_callback)
        glfw.set_window_size_callback(window, self._window_size_callback)

        glfw.set_key_callback(window, self._key_callback)
        glfw.set_char_callback(window, self._char_callback)

        return window
        
    def _cursor_pos_callback(self, window, xpos, ypos):
        self._current_vp = self.vp_intersect(xpos, ypos)

        if self.imgui.want_mouse:
            return

        vp = self.viewports[self.current_vp]
        vp.cursor_pos_callback(vp.idx, xpos, ypos)

    def _mouse_button_callback(self, window, button, action, mods):        
        if self.imgui.want_mouse:
            return

        vp = self.viewports[self.current_vp]
        vp.mouse_button_callback(vp.idx, button, action, mods)

    def _scroll_callback(self, window, xoffset, yoffset):
        if self.imgui.want_mouse:
            return
        
        vp = self.viewports[self.current_vp]
        vp.scroll_callback(vp.idx, xoffset, yoffset)

    def _window_size_callback(self, window, width, height):
        vp = self.viewports[self.current_vp]
        vp.window_size_callback(vp.idx, width, height)

        # TODO: CALL viewport resize

    def _key_callback(self, *args, **kwargs):
        if self.imgui.want_keyboard:
            self.ui.impl.keyboard_callback(*args, **kwargs)
            return

        vp = self.viewports[self.current_vp]
        vp.key_callback(*args, **kwargs)

    def _char_callback(self, *args, **kwargs):
        if self.imgui.want_keyboard:
            self.ui.impl.keyboard_callback(*args, **kwargs)
            return

        vp = self.viewports[self.current_vp]
        vp.char_callback(*args, **kwargs)

    def add_viewport(self, width, height):
        vp_new = Viewport(self.vp_count)
        self.viewports.append(vp_new)

        self.vp_count += 1
        vp_w = self.width // self.vp_count

        for i, vp in enumerate(self.viewports):
            vp.width = vp_w
            vp.xpos = vp_w * i

        return vp_new
    
    def vp_intersect(self, xpos, ypos):
        idx = int(xpos / self.width * self.vp_count)

        return min(idx, self.vp_count - 1)

        # for vp in self.viewports:
        #     x_in = vp.xpos <= xpos <= (vp.xpos + vp.width)
        #     y_in = vp.ypos <= ypos <= (vp.ypos + vp.height)

        #     if x_in and y_in:
        #         return vp.idx

        # return 0

    @property
    def current_vp(self):
        return self._current_vp

    def set_cursor_pos_callback(self, vp, fn):
        vp_id = vp.idx
        self.viewports[vp_id].cursor_pos_callback = fn

    def set_mouse_button_callback(self, vp, fn):
        vp_id = vp.idx
        self.viewports[vp_id].mouse_button_callback = fn

    def set_scroll_callback(self, vp, fn):
        vp_id = vp.idx
        self.viewports[vp_id].scroll_callback = fn

    def set_window_size_callback(self, vp,fn):
        vp_id = vp.idx
        self.viewports[vp_id].window_size_callback = fn

    def set_key_callback(self, vp, fn):
        vp_id = vp.idx
        self.viewports[vp_id].key_callback = fn

    def set_char_callback(self, vp, fn):
        vp_id = vp.idx
        self.viewports[vp_id].char_callback = fn

    def set_on_render(self, vp, fn):
        vp_id = vp.idx
        self.viewports[vp_id].on_render = fn


class Viewport:
    def __init__(self, idx):
        self._idx = idx

        self.xpos = None
        self.ypos = None
        self.width = None
        self.height = None

        self.cursor_pos_callback = None
        self.mouse_button_callback = None
        self.scroll_callback = None
        self.window_size_callback = None
        self.key_callback = None
        self.char_callback = None

        self.on_render = None

    @property
    def idx(self):
        return self._idx

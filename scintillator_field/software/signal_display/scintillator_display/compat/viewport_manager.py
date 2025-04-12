import glfw
import imgui

from OpenGL.GL import glViewport, glEnable, GL_SCISSOR_TEST, glScissor, glDisable
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
        self.vp_current = 0

        self.vp_focus = 0
        self.vp_focused = False

        self.imgui = ImguiManager(self.window)

    def render_loop(self):
        self.vp_resize(vp_resize_callback=True)
        glEnable(GL_SCISSOR_TEST)

        while not glfw.window_should_close(self.window):
            imgui.new_frame()

            for vp in self.viewports:
                glViewport(vp.xpos, vp.ypos, vp.width, vp.height)
                glScissor(vp.xpos, vp.ypos, vp.width, vp.height)
                vp.on_render()

            imgui.render()
            self.imgui.impl.process_inputs()
            self.imgui.impl.render(imgui.get_draw_data())

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glDisable(GL_SCISSOR_TEST)
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
    
    def get_focused_vp(self):
        return self.vp_focus if self.vp_focused else self.vp_current

    def _cursor_pos_callback(self, window, xpos, ypos):
        self.vp_current = self.vp_intersect(xpos, ypos)

        if self.imgui.want_mouse:
            return

        vp = self.viewports[self.get_focused_vp()]
        vp.cursor_pos_callback(vp, xpos, ypos)

    def _mouse_button_callback(self, window, button, action, mods):        
        if self.imgui.want_mouse:
            return
        
        self.vp_focused = action == glfw.PRESS
        if not self.vp_focused:
            deselect_vp = self.viewports[self.vp_focus]
            deselect_vp.mouse_button_callback(deselect_vp, button, glfw.RELEASE, mods)

        self.vp_focus = self.vp_current

        vp = self.viewports[self.get_focused_vp()]
        vp.mouse_button_callback(vp, button, action, mods)

    def _scroll_callback(self, window, xoffset, yoffset):
        if self.imgui.want_mouse:
            return
        
        vp = self.viewports[self.get_focused_vp()]
        vp.scroll_callback(vp, xoffset, yoffset)

    def _window_size_callback(self, window, width, height):
        self.width = width
        self.height = height
        self.vp_resize(vp_resize_callback=True)

    def _key_callback(self, *args, **kwargs):
        if self.imgui.want_keyboard:
            self.ui.impl.keyboard_callback(*args, **kwargs)
            return

        vp = self.viewports[self.get_focused_vp()]
        vp.key_callback(*args, **kwargs)

    def _char_callback(self, *args, **kwargs):
        if self.imgui.want_keyboard:
            self.ui.impl.keyboard_callback(*args, **kwargs)
            return

        vp = self.viewports[self.get_focused_vp()]
        vp.char_callback(*args, **kwargs)

    def add_viewport(self, width, height):
        vp_new = Viewport(self.vp_count)
        self.viewports.append(vp_new)

        self.vp_count += 1
        self.vp_resize()

        return vp_new
    
    def vp_resize(self, vp_resize_callback=False):
        vp_w = self.width // self.vp_count

        for i, vp in enumerate(self.viewports):
            vp.width = vp_w
            vp.height = self.height

            vp.xpos = vp_w * i
            vp.ypos = 0

            if vp_resize_callback:
                vp.window_size_callback(vp, vp.width, vp.height)
    
    def vp_intersect(self, xpos, ypos):
        idx = int(xpos / self.width * self.vp_count)

        return min(idx, self.vp_count - 1)

        # for vp in self.viewports:
        #     x_in = vp.xpos <= xpos <= (vp.xpos + vp.width)
        #     y_in = vp.ypos <= ypos <= (vp.ypos + vp.height)

        #     if x_in and y_in:
        #         return vp.idx

        # return 0

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

        self._cursor_pos_callback = None
        self._mouse_button_callback = None
        self._scroll_callback = None
        self._window_size_callback = None
        self._key_callback = None
        self._char_callback = None

        self._on_render = None

    @property
    def idx(self):
        return self._idx
    
    def null_callback(self, *args, **kwargs):
        ...
    
    @property
    def cursor_pos_callback(self):
        if self._cursor_pos_callback:
            return self._cursor_pos_callback

        return self.null_callback

    @cursor_pos_callback.setter
    def cursor_pos_callback(self, fn):
        self._cursor_pos_callback = fn

    @property
    def mouse_button_callback(self):
        if self._mouse_button_callback:
            return self._mouse_button_callback
        return self.null_callback

    @mouse_button_callback.setter
    def mouse_button_callback(self, fn):
        self._mouse_button_callback = fn

    @property
    def scroll_callback(self):
        if self._scroll_callback:
            return self._scroll_callback
        return self.null_callback

    @scroll_callback.setter
    def scroll_callback(self, fn):
        self._scroll_callback = fn

    @property
    def window_size_callback(self):
        if self._window_size_callback:
            return self._window_size_callback
        return self.null_callback

    @window_size_callback.setter
    def window_size_callback(self, fn):
        self._window_size_callback = fn

    @property
    def key_callback(self):
        if self._key_callback:
            return self._key_callback
        return self.null_callback

    @key_callback.setter
    def key_callback(self, fn):
        self._key_callback = fn

    @property
    def char_callback(self):
        if self._char_callback:
            return self._char_callback
        return self.null_callback

    @char_callback.setter
    def char_callback(self, fn):
        self._char_callback = fn

    @property
    def on_render(self):
        if self._on_render:
            return self._on_render
        return self.null_callback

    @on_render.setter
    def on_render(self, fn):
        self._on_render = fn

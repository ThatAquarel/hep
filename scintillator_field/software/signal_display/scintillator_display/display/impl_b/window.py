import time


# import glfw
import scintillator_display.compat.glfw as glfw


from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


from scintillator_display.display.impl_b.opengl_stuff import OpenGLStuff

from scintillator_display.display.camera_shader_controls import CameraShaderControls




class Window:
    def __init__(self):

        self.cam_shader = CameraShaderControls(zoom=90)
        
        self.data_boxes_checked = []

        self.pause_time = time.time()

    def build_window(self, window_name):
        
        window = glfw.create_window(self.cam_shader.width, self.cam_shader.height, window_name, None, None)
        glfw.make_context_current(window)
        # glfw.get_framebuffer_size(window)
        self.set_callbacks(window)

        return window

    def set_callbacks(self, window):
        glfw.set_key_callback(window, self.key_callbacks)
        glfw.set_mouse_button_callback(window, self.mouse_callbacks)
        glfw.set_cursor_pos_callback(window, self.cursor_pos_callbacks)
        glfw.set_scroll_callback(window, self.scroll_callbacks)
        glfw.set_window_size_callback(window, self.window_callbacks)
    
    def window_callbacks(self, window, width, height):
        if not (width==0 or height==0):
            self.cam_shader.width, self.cam_shader.height = width, height
            self.cam_shader.zoom = self.cam_shader.zoom*self.cam_shader.aspect_ratio*self.cam_shader.height/self.cam_shader.width
            self.cam_shader.aspect_ratio = width/height

            glViewport(0, 0, width, height)
            # will be changed to double viewport later


    def scroll_callbacks(self, window, xoffset, yoffset):
        scroll_amount = self.cam_shader.zoom/27.5 if self.cam_shader.zoom/27.5 > 0.24 else 0.24

        if ((self.cam_shader.zoom-scroll_amount*yoffset != 0)
                and not
            ((self.cam_shader.zoom-scroll_amount*yoffset > -0.1)
                and
             (self.cam_shader.zoom-scroll_amount*yoffset < 0.1))):
            self.cam_shader.zoom -= scroll_amount*yoffset
    
    def cursor_pos_callbacks(self, window, xpos, ypos):
        if self.cam_shader.panning:
            dx = xpos - self.cam_shader.last_x
            dy = ypos - self.cam_shader.last_y
            self.cam_shader.pan_x += dx * self.cam_shader.pan_sensitivity * self.cam_shader.zoom
            self.cam_shader.pan_y -= dy * self.cam_shader.pan_sensitivity * self.cam_shader.zoom

        if self.cam_shader.angling:
            dx = xpos - self.cam_shader.last_x
            dy = ypos - self.cam_shader.last_y
            self.cam_shader.angle_x += dy * self.cam_shader.angle_sensitivity * self.cam_shader.zoom
            self.cam_shader.angle_y += dx * self.cam_shader.angle_sensitivity * self.cam_shader.zoom

            self.cam_shader.angle_x %= 360
            self.cam_shader.angle_y %= 360
            self.cam_shader.angle_z %= 360


        self.cam_shader.last_x, self.cam_shader.last_y = xpos, ypos
    
    def mouse_callbacks(self, window, button, action, mods):

        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.cam_shader.panning = True
            elif button == glfw.MOUSE_BUTTON_RIGHT: # Dual-viewports: glfw namespace change
                self.cam_shader.angling = True
        if action == glfw.RELEASE:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.cam_shader.panning = False
            elif button == glfw.MOUSE_BUTTON_RIGHT: # Dual-viewports: glfw namespace change
                self.cam_shader.angling = False
    
    def key_callbacks(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                glfw.terminate()
                self.done = True
            if (key == glfw.KEY_SPACE) and (not self.paused):
                self.paused = True
                self.pause_time = time.time()
            if (key == glfw.KEY_SPACE) and (self.paused) and (time.time()- self.pause_time > 0.01):
                self.paused = False

    def main(self):
        if not glfw.init():
            return


        appname = type(self).__name__
        self.window = self.build_window(appname)
        

        self.opengl_stuff_for_window = OpenGLStuff(self.cam_shader)
        self.opengl_stuff_for_window.setup()

        self.data_boxes_checked = self.opengl_stuff_for_window.arduino.impl_b_data_is_checked

        self.done = False
        self.paused = False

        while not (self.done or glfw.window_should_close(self.window)): # Dual-viewports: need reference to glfw.
            self.render_loop()


    def render_loop(self):

        self.opengl_stuff_for_window.per_render_loop(self)

        glfw.swap_buffers(self.window)
        glfw.poll_events()

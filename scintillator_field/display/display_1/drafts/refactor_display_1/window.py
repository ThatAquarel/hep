import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import imgui
from imgui.integrations.glfw import GlfwRenderer

import numpy as np

import time



class Window:
    def __init__(self):
        pass

    def set_window_values(self):

        # sets up basic window parameters

        self.render_distance = 1024
        
        self.width, self.height = 1924, 1028
        #self.width, self.height = 750, 500
        self.aspect_ratio = self.width/self.height

        self.angle_x, self.angle_y, self.angle_z = 0, 0, 45
        self.pan_x, self.pan_y, self.pan_z = 0, 0, 0

        self.last_x, self.last_y = 0, 0
        self.zoom = 5
        


        # self.angle_x, self.angle_y, self.angle_z = 67.3, -73.1, 45
        self.angle_x, self.angle_y, self.angle_z = 15,-45,0
        self.pan_x, self.pan_y, self.pan_z = 0,0,0
        self.zoom = 14.1
        self.zoom = 231

        #self.angle_x, self.angle_y, self.angle_z = (0,)*3



        self.pan_sensitivity = 0.001
        self.angle_sensitivity = 0.01

        self.panning, self.angling = False, False

    def setup_imgui(self, window, appname):
        self.appname = appname
        imgui.create_context()
        imgui.get_io().display_size = 100,100
        self.imgui_use = GlfwRenderer(window, attach_callbacks=False)

    def set_imgui_box_per_render(self, dt, paused):
        imgui.new_frame()
        imgui.begin(self.appname)

        if not paused:
            if dt != 0:
                imgui.text(f'{1/dt:.4g} fps')
        else:
            imgui.text(f"paused ({1/dt:.4g} fps)")

        imgui.text(f'{self.angle_x:.3g}, {self.angle_y:.3g}, {self.angle_z:.3g} : angles x, y, z')
        imgui.text(f'{self.pan_x:.3g}, {self.pan_y:.3g}, {self.pan_z:.3g} : pan x, y, z')
        imgui.text(f'{self.zoom:.3g} : zoom level')
        imgui.text(f'{self.aspect_ratio:.3g} : aspect ratio')

        imgui.end()

    def imgui_in_use(self):
        if self.imgui_use != None and imgui.get_io().want_capture_mouse:
            return True
        
    def render_imgui_box(self):
        imgui.render()
        self.imgui_use.process_inputs()
        self.imgui_use.render(imgui.get_draw_data())

    def build_window(self, window_name):

        if not glfw.init():
            return
        
        window = glfw.create_window(self.width, self.height, window_name, None, None)
        glfw.make_context_current(window)
        glfw.get_framebuffer_size(window)
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
            self.width, self.height = width, height
            self.zoom = self.zoom*self.aspect_ratio*self.height/self.width
            self.aspect_ratio = width/height

            glViewport(0, 0, width, height)
            # will be changed to double viewport later


    def scroll_callbacks(self, window, xoffset, yoffset):
        if (self.zoom-0.24*yoffset != 0) and not ((self.zoom-0.24*yoffset > -0.1) & (self.zoom-0.24*yoffset < 0.1)):
            self.zoom -= 0.24*yoffset
    
    def cursor_pos_callbacks(self, window, xpos, ypos):
        if self.panning:
            dx = xpos - self.last_x
            dy = ypos - self.last_y
            self.pan_x += dx * self.pan_sensitivity * self.zoom
            self.pan_y -= dy * self.pan_sensitivity * self.zoom

        if self.angling:
            dx = xpos - self.last_x
            dy = ypos - self.last_y


            self.angle_x += dy * self.angle_sensitivity * self.zoom
            self.angle_y += dx * self.angle_sensitivity * self.zoom



            self.angle_x += dy * self.angle_sensitivity * self.zoom
            self.angle_y += dx * self.angle_sensitivity * self.zoom


            self.angle_x %= 360
            self.angle_y %= 360
            self.angle_z %= 360


        self.last_x, self.last_y = xpos, ypos
    
    def mouse_callbacks(self, window, button, action, mods):
        # stops screen panning/rotating if imgui box is moving
        if self.imgui_in_use():
            return

        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.panning = True
            elif button == GLFW_MOUSE_BUTTON_RIGHT:
                self.angling = True
        if action == glfw.RELEASE:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.panning = False
            elif button == GLFW_MOUSE_BUTTON_RIGHT:
                self.angling = False
    
    def key_callbacks(self, window, key, scancode, action, mods):
        global pause_time
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                glfw.terminate()
                self.done = True
            if (key == glfw.KEY_SPACE) and (not self.paused):
                self.paused = True
                pause_time = time.time()
            if (key == glfw.KEY_SPACE) and (self.paused) and (time.time()- pause_time > 0.01):
                self.paused = False


    def set_opengl_values(self):
        
        glClearColor(0.5, 0.5, 0.5, 1)
        glEnable(GL_DEPTH_TEST)

        # antialiasing (smoother lines)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_POINT_SMOOTH)

        # opacity
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

    def begin_render_loop_actions(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def end_render_loop_actions(self, window):
        glfw.swap_buffers(window)
        glfw.poll_events()
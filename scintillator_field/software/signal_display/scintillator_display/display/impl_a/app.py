import time
from datetime import datetime

# import glfw
import scintillator_display.compat.glfw as glfw

import glm
# import imgui
import scintillator_display.compat.imgui as imgui

import pandas as pd

from  scintillator_display.display.impl_ab_data_input_manager import Data
from scintillator_display.display.xyz_axes import Axes

import scintillator_display.display.impl_a.graphics.scintillator_structure as scintillator_structure

from scintillator_display.display.camera_shader_controls import CameraShaderControls

from OpenGL.GL import *


class App():
    def __init__(
        self,
        window_size,
    ):
        """
        Joule App: Main class for application

        Extends: CameraOrbitControls, ShaderRenderer

        :param window_size: Initial window size (width, height)
        :param name: Initial window name
        """


        # initialize window
        self.window = self.window_init(window_size)

        self.cam_shader = CameraShaderControls(angle_sensitivity=0.1,zoom=25, clear_colour=(0.87,)*3)
        scale = 12

        #setup elements

        self.data_manager = Data(impl_constant=0.1, impl="a",
                                 hull_colour=[1, 0, 0], hull_opacity=0.3,
                                 store_normals=True)
        self.plane = scintillator_structure.Plane(data_manager=self.data_manager, scale=scale)
        #self.xyz_axes = Axes(l=scale/2)
        self.xyz_axes = Axes(l=4*scale)


        self.pt_selected = None
        self.dataset_active = None
        self.show_axes = True


        # fall into rendering loop
        self.rendering_loop()


    def window_init(self, window_size):
        # throw exception if glfw failed to init
        if not glfw.init():
            raise Exception("GLFW could not be initialized.")

        # enable multisampling (antialiasing) on glfw window
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        #glfw.window_hint(glfw.SAMPLES, 4)

        # create window and context
        window = glfw.create_window(*window_size, None, None, None)
        if not window:
            glfw.terminate()
            raise Exception("GLFW window could not be created.")
        glfw.make_context_current(window)

        # wrapper callback functions to dispatch events to ui and camera
        glfw.set_cursor_pos_callback(window, self.cursor_pos_callback)
        glfw.set_mouse_button_callback(window, self.mouse_button_callback)
        glfw.set_scroll_callback(window, self.scroll_callback)
        glfw.set_framebuffer_size_callback(window, self.resize_callback)


        return window
    
    # NOTE : FIX THESE
    
    def mouse_button_callback(self, window, button, action, mods):
        # filter for right clicks which are
        # for camera movements
        if button != glfw.MOUSE_BUTTON_RIGHT:
            return

        # dragging when: right mouse button held
        self.cam_shader.mouse_dragging = action == glfw.PRESS

        # panning when: ctrl + right mouse button held
        self.cam_shader.panning = glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS

        # add ball: left click
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            pass
            #self.on_click(window)

    def cursor_pos_callback(self, window, xpos, ypos):
        if self.cam_shader.mouse_dragging:

            # change in mouse position over one frame
            dx = xpos - self.cam_shader.last_x
            dy = ypos - self.cam_shader.last_y

            if self.cam_shader.panning:
                # adjust pan according to zoom
                # so that translation is always constant,
                # independent of zoom
                zoomed_pan = self.cam_shader.pan_sensitivity * self.cam_shader.zoom

                # updates translation vector
                # [1, -1] flips the y position as OpenGL's origin
                # is at the bottom left corner instead of top left
                self.cam_shader.pan_x += dx * zoomed_pan
                self.cam_shader.pan_y -= dy * zoomed_pan
            else:

                # updates rotation vector
                # [::-1] reverses the order, effectively mapping the
                # x screen position onto the OpenGL's x rotation and
                # y screen position onto the OpenGL's y rotation
                self.cam_shader.angle_x += dy * self.cam_shader.angle_sensitivity
                self.cam_shader.angle_y += dx * self.cam_shader.angle_sensitivity

        # save previous to calculate the next delta
        self.cam_shader.last_x, self.cam_shader.last_y = xpos, ypos

    def scroll_callback(self, window, xoffset, yoffset):
        scroll_amount = self.cam_shader.zoom/27.5 if self.cam_shader.zoom/27.5 > 0.24 else 0.24

        if ((self.cam_shader.zoom-scroll_amount*yoffset != 0)
                and not
            ((self.cam_shader.zoom-scroll_amount*yoffset > -0.1)
                and
             (self.cam_shader.zoom-scroll_amount*yoffset < 0.1))):
            self.cam_shader.zoom -= scroll_amount*yoffset

    def resize_callback(self, window, width, height):
        # update rendering shape
        glViewport(0, 0, width, height)
        self.cam_shader.width, self.cam_shader.height = width, height

        # compute aspect ratio, so that the render
        # is not stretched if the window is stretched
        # bugfix: on X11 Ubuntu 20.04, the height starts
        # at zero when the window is first rendered, so we
        # prevent a zero division error
        self.cam_shader.aspect_ratio = width / height if height > 0 else 1.0

    def window_should_close(self):
        return glfw.window_should_close(self.window)

    def rendering_loop(self):
        """
        Main rendering loop for application
        """

        self.cam_shader.make_shader_program()
        self.cam_shader.setup_opengl()

        start = time.time()
        dt = 0

        # main rendering loop until user quits
        while not self.window_should_close():


            # call rendering
            self.on_render_frame()


            glfw.swap_buffers(self.window)
            glfw.poll_events()

            # compute dt for integration
            current = time.time()
            dt = current - start
            start = current

        if not self.data_manager.debug:
            self.generate_csv()

        glfw.terminate()


    
    def on_render_frame(self):
        """
        Render frame event callback
        """

        self.cam_shader.begin_render_gl_actions()



        #chekc arduino if there's data; gather data if there is
        if self.data_manager.arduino_has_data():
            if self.data_manager.is_valid_data():
                self.data_manager.transform_data_per_impl()
        


        #input for drawing
        self.dataset_active = self.data_manager.impl_a_data_is_checked

        
        #draw elements
        self.data_manager.draw_active_hulls(self.data_manager.data, self.dataset_active)

        if self.show_axes:
            self.xyz_axes.draw()
        
        self.plane.draw(self.pt_selected)
    
        
      
    def generate_csv(self):
        """
        Create csv file
        """
        
        df = pd.DataFrame(self.data_manager.data,columns=["new_hull_bounds", "cooked_data", "bit24", "time"])

        df = df.drop("new_hull_bounds", axis=1)
        df = df.drop("cooked_data", axis=1)

        time = datetime.now()
        time = ("").join([t if t != ":" else "." for t in str(time) ])

        try:
            df.to_csv(f"scintillator_display/data/{time}.csv")   #Current directory is set to the "data" folder
        except:
            df.to_csv(f"{time}.csv")
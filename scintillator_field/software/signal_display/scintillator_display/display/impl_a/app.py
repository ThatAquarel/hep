import time
from datetime import datetime

# import glfw
import scintillator_display.compat.glfw as glfw

import glm
# import imgui
import scintillator_display.compat.imgui as imgui

import pandas as pd

import scintillator_display.display.impl_a.graphics as graphics
import scintillator_display.display.impl_a.data_manager as data_manager

import scintillator_display.display.impl_a.graphics.elements.axes as axes
import scintillator_display.display.impl_a.graphics.elements.square as square
import scintillator_display.display.impl_a.graphics.elements.trajectory as trajectory
import scintillator_display.display.impl_a.graphics.elements.fan as fan
import scintillator_display.display.impl_a.graphics.elements.plane as plane

from scintillator_display.display.impl_a.graphics.orbit_controls import CameraOrbitControls
from scintillator_display.display.impl_a.graphics.parameter_interface import ParameterInterface
from scintillator_display.display.impl_a.graphics.shader_renderer import ShaderRenderer


class App(CameraOrbitControls, ShaderRenderer):
    def __init__(
        self,
        window_size,
        name,
        *orbit_control_args,
    ):
        """
        Joule App: Main class for application

        Extends: CameraOrbitControls, ShaderRenderer

        :param window_size: Initial window size (width, height)
        :param name: Initial window name
        """

        # init camera orbit controls and shader renderer
        super().__init__(*orbit_control_args)

        # initialize window
        self.window = self.window_init(window_size, name)

        # initialize ui
        self.ui = ParameterInterface(
            self.window,
        )

        self.scale = 12

        #setup elements
        self.plane = plane.Plane(scale = self.scale)
        self.square = square.square(scale = self.scale)
        self.trajectory = trajectory.trajectory(scale = self.scale)
        self.axes = axes.Axes(self.scale,self.scale)
        self.fan = fan.Fan(scale = self.scale)

        self.test = data_manager.test()


        self.pt_selected = None


        # fall into rendering loop
        self.rendering_loop()

    def window_init(self, window_size, name):
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
        window = glfw.create_window(*window_size, name, None, None)
        if not window:
            glfw.terminate()
            raise Exception("GLFW window could not be created.")
        glfw.make_context_current(window)

        # wrapper callback functions to dispatch events to ui and camera
        glfw.set_cursor_pos_callback(window, self.cursor_pos_callback)
        glfw.set_mouse_button_callback(window, self.mouse_button_callback)
        glfw.set_scroll_callback(window, self.scroll_callback)
        glfw.set_framebuffer_size_callback(window, self.resize_callback)

        glfw.set_key_callback(window, self.key_callback)
        glfw.set_char_callback(window, self.char_callback)

        # initially call window resize to rescale frame
        self.camera_resize_callback(window, *window_size)

        return window

    def key_callback(self, *args):
        # forward ui keyboard callbacks
        if self.ui.want_keyboard:
            self.ui.impl.keyboard_callback(*args)

    def char_callback(self, *args):
        # forward ui keyboard callbacks
        if self.ui.want_keyboard:
            self.ui.impl.char_callback(*args)

    def mouse_button_callback(self, window, button, action, mods):
        # forward ui mouse callbacks
        if self.ui.want_mouse:
            return

        # forward camera mouse callbacks
        self.camera_mouse_button_callback(window, button, action, mods)

        # add ball: left click
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            pass
            #self.on_click(window)

    def cursor_pos_callback(self, window, xpos, ypos):
        # forward ui mouse callbacks
        if self.ui.want_mouse:
            return

        # forward camera mouse callbacks
        self.camera_cursor_pos_callback(window, xpos, ypos)

    def scroll_callback(self, window, xoffset, yoffset):
        # forward ui mouse callbacks
        if self.ui.want_mouse:
            return

        # forward camera mouse callbacks
        self.camera_scroll_callback(window, xoffset, yoffset)

    def resize_callback(self, window, width, height):
        # forward camera window callback
        self.camera_resize_callback(window, width, height)

    def window_should_close(self):
        return glfw.window_should_close(self.window)

    def rendering_loop(self):
        """
        Main rendering loop for application
        """

        self.render_setup()

        start = time.time()
        dt = 0

        # main rendering loop until user quits
        while not self.window_should_close():


            # call rendering
            self.on_render_frame()
            self.ui.on_render_ui(self.window,self.pt_selected)

            self.ui.impl.process_inputs()
            self.ui.impl.render(imgui.get_draw_data())


            glfw.swap_buffers(self.window)
            glfw.poll_events()

            # compute dt for integration
            current = time.time()
            dt = current - start
            start = current

        self.generate_csv()

        glfw.terminate()


    
    def on_render_frame(self):
        """
        Render frame event callback
        """

        # setup frame rendering with OpenGL calls
        self.frame_setup(self.ui.background_color)

        # shader: update camera matrices
        self.set_matrix_uniforms(
            self.get_camera_projection(),
            self.get_camera_transform(),
        )


        #chekc arduino if there's data; gather data if there is
        if self.test.has_data():
            self.test.update_data(self.test.get_data_from_arduino())
        


        #input for drawing
        self.ui.input_data = self.test.data.copy()

        
        #draw elements
        self.square.draw(self.test.data.copy(), self.ui.dataset_active)
        self.fan.draw(self.test.data.copy(), self.ui.dataset_active)

        if self.ui.show_axes:
            self.axes.draw()
            
        self.plane.draw(self.ui.pt_selected)
    

        
        # shader: update lighting
        self.set_lighting_uniforms(
            glm.vec3(*self.ui.light_color),
            ambient_strength=self.ui.ambient_strength,
            diffuse_strength=self.ui.diffuse_strength,
            diffuse_base=self.ui.diffuse_base,
            specular_strength=self.ui.specular_strength,
            specular_reflection=self.ui.specular_reflection,
        )




    # def on_click(self, window):
    #     # get 3D click coordinates
    #     rh = self.get_right_handed()
    #     self.x, self.y, self.z = self.get_click_point(window, rh)
        

    #     print(self.x, self.y, self.z)
    #     uncertainty = 1
    #     for i in range(len(self.test.data)):
    #         #To see if the mouse position matches 
    #         if self.ui.dataset_active[i]:
    #             for pt in range(len(self.test.data[i])):     #test.data -> datasets -> cubes -> vertices or fan -> coords -> xyz values
    #                 if (self.test.data[i][pt][0][0][0] <= (self.x + uncertainty)) and (self.test.data[i][pt][0][0][0] >= (self.x - uncertainty)):
    #                     if (self.test.data[i][pt][0][0][1] <= (self.y + uncertainty)) and (self.test.data[i][pt][0][0][1] >= (self.y - uncertainty)):
    #                         self.pt_selected = self.test.data[i][pt]
      
    def generate_csv(self):
        """
        Create csv file
        """
        
        df = pd.DataFrame(self.test.data,columns=["new_hull_bounds", "new_fan_out_lines", "cooked_data", "bit24", "time"])

        df = df.drop("new_hull_bounds", axis=1)
        df = df.drop("new_fan_out_lines", axis=1)
        df = df.drop("cooked_data", axis=1)

        #df.columns[0], df.columns[1] = df.columns[1], df.columns[0] 
        time = datetime.now()
        time = ("").join([t if t != ":" else "." for t in str(time) ])

        try:
            df.to_csv(f"scintillator_display/data/{time}.csv")   #Current directory is set to the "data" folder
        except:
            df.to_csv(f"{time}.csv")

        



        


def run():
    # run the app
    App((1280, 720), "Not Joule")

# run()

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from scintillator_display.display.camera_shader_controls import CameraShaderControls

from scintillator_display.display.impl_b.scintillator_blocks import ScintillatorStructure

from scintillator_display.display.vao_vbo import create_vao, update_vbo, draw_vao

from scintillator_display.display.xyz_axes import Axes

from scintillator_display.display.impl_ab_data_input_manager import Data

class OpenGLStuff:
    def __init__(self, camera_shader:CameraShaderControls):
        # class initialisation, nothing goes here
        self.cam_shader = camera_shader


    def setup(self):
        # setup of all elements to be rendered on each loop

        self.pt_selected = None

        self.arduino = Data(impl_constant=1, impl="b",
                            hull_colour=[0.5, 0, 0.5], hull_opacity=0.8,
                            store_normals=True)


        self.scintillator_structure = ScintillatorStructure(self.arduino)


        self.cam_shader.make_shader_program()
        self.cam_shader.setup_opengl()

        
        self.xyz_axes = Axes(l=250)

        self.data_exists = False
        self.new_data = False


        self.show_axes = True



        pass

    def per_render_loop(self, window):
        # draw on-loop actions




        self.cam_shader.begin_render_gl_actions()







        if not self.arduino.debug:
            #if self.detected_hulls.arduino.arduino_has_data():
            #    if self.detected_hulls.arduino.is_valid_data():
            #        hull_bounds = self.detected_hulls.arduino.transform_data_per_impl()
            #        self.detected_hulls.create_hull_data(hull_bounds)
            #
            #if self.detected_hulls.new_data:
            #    self.detected_hulls.create_hull_vao()
            #
            #self.detected_hulls.new_data = False
            #
            #if self.detected_hulls.data_exists:
            #    self.detected_hulls.draw_hull()
            pass
            # NOTE : MUST FIX THIS
        
        elif self.arduino.debug:
            pass
            self.arduino.draw_active_hulls(self.arduino.data, self.arduino.impl_b_data_is_checked)



        self.scintillator_structure.reset_scintillator_colour()
        
        




        if self.pt_selected != None:
            self.scintillator_structure.recolour_for_point(self.pt_selected)



        self.scintillator_structure.renew_vbo()


        self.scintillator_structure.draw_scintillator_structure()

        if self.show_axes:
            self.xyz_axes.draw()

        pass
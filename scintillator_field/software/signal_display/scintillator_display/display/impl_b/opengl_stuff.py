from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from scintillator_display.display.impl_b.shaders.shaders import *

from scintillator_display.display.impl_b.scintillator_blocks import ScintillatorStructure


from scintillator_display.display.vao_vbo import create_vao, update_vbo, draw_vao

from scintillator_display.display.xyz_axes import Axes

from scintillator_display.display.impl_ab_data_input_manager import Data

class OpenGLStuff:
    def __init__(self):
        # class initialisation, nothing goes here
        pass


    def setup(self):
        # setup of all elements to be rendered on each loop

        self.arduino = Data(impl_constant=1, impl="b",
                            hull_colour=[0.5, 0, 0.5], hull_opacity=0.8,
                            store_normals=False)


        self.scintillator_structuce = ScintillatorStructure(self.arduino)


        self.shader_program = make_shaders()



        
        self.xyz_axes = Axes(l=250)

        self.data_exists = False
        self.new_data = False


        self.show_axes = True



        pass

    def per_render_loop(self, window):
        # draw on-loop actions


        glUseProgram(self.shader_program)

        make_uniforms(self.shader_program, window)












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
            self.arduino.draw_active_hulls(self.arduino.data, self.arduino.impl_b_data_is_checked)




        self.scintillator_structuce.draw_scintillator_structure()

        if self.show_axes:
            self.xyz_axes.draw()

        pass
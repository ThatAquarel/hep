from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from scintillator_field.display.display_1.vbo_vao_stuff import *
from scintillator_field.display.display_1.shaders.shaders import *

from scintillator_field.display.display_1.scintillator_blocks import *
from scintillator_field.display.display_1.detection_display import *


class OpenGLStuff:
    def __init__(self):
        # class initialisation, nothing goes here
        pass


    def setup(self):
        # setup of all elements to be rendered on each loop


        self.scintillator_structuce = ScintillatorStructure()
        self.detected_hulls = DetectionHulls()


        self.shader_program = make_shaders()

        pass

    def per_render_loop(self, window):
        # draw on-loop actions


        glUseProgram(self.shader_program)

        make_uniforms(self.shader_program, window)

        self.detected_hulls.data_exists = False
        self.detected_hulls.new_data = False



        if self.detected_hulls.arduino.has_new_data():
            self.detected_hulls.create_hull_data()

        if self.detected_hulls.new_data:
            self.detected_hulls.create_hull_vao()

        if self.detected_hulls.data_exists:
            self.detected_hulls.draw_hull()

        self.scintillator_structuce.draw_scintillator_structure()


        pass
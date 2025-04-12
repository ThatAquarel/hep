from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

# from scintillator_field.display.display_1.vbo_vao_stuff import *
from scintillator_display.display.impl_b.vbo_vao_stuff import *

# from scintillator_field.display.display_1.shaders.shaders import *
from scintillator_display.display.impl_b.shaders.shaders import *

# from scintillator_field.display.display_1.scintillator_blocks import *
from scintillator_display.display.impl_b.scintillator_blocks import ScintillatorStructure

# from scintillator_field.display.display_1.detection_display import *
from scintillator_display.display.impl_b.detection_display import DetectionHulls


class OpenGLStuff:
    def __init__(self):
        # class initialisation, nothing goes here
        pass


    def setup(self):
        # setup of all elements to be rendered on each loop


        self.scintillator_structuce = ScintillatorStructure()
        self.detected_hulls = DetectionHulls()


        self.shader_program = make_shaders()



        # self.lines = np.array([
        #     [ 0, 0,   -81, 1, 0, 0, 1],
        #     [25, 0,   -81, 1, 0, 0, 1],
        #     [ 0, 0,   -81, 0, 1, 0, 1],
        #     [0, 25,   -81, 0, 1, 0, 1],
        #     [ 0, 0,   -81, 0, 0, 1, 1],
        #     [0,  0, 25-81, 0, 0, 1, 1],
        # ]).astype(np.float32)

        
        self.lines = np.array([
            [ 0, 0,   0, 1, 0, 0, 1],
            [250, 0,   0, 1, 0, 0, 1],
            [ 0, 0,   0, 0, 1, 0, 1],
            [0, 250,   0, 0, 1, 0, 1],
            [ 0, 0,   0, 0, 0, 1, 1],
            [0,  0,  250, 0, 0, 1, 1],
        ]).astype(np.float32)

        self.lines_vao = make_vao_vbo(self.lines)[0]

        self.detected_hulls.data_exists = False
        self.detected_hulls.new_data = False




        pass

    def per_render_loop(self, window):
        # draw on-loop actions


        glUseProgram(self.shader_program)

        make_uniforms(self.shader_program, window)




        if self.detected_hulls.arduino.has_new_data():
            self.detected_hulls.create_hull_data()

        if self.detected_hulls.new_data:
            self.detected_hulls.create_hull_vao()

        self.detected_hulls.new_data = False

        if self.detected_hulls.data_exists:
            self.detected_hulls.draw_hull()

        self.scintillator_structuce.draw_scintillator_structure()

        #draw_vao(self.lines_vao, GL_LINES, self.lines.shape[0])


        pass
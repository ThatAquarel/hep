import numpy as np

import time


from scintillator_field.display.display_1.drafts.refactor_attempt_1.window import Window
from scintillator_field.display.display_1.drafts.refactor_attempt_1.vbo_vao_stuff import *
from scintillator_field.display.display_1.drafts.refactor_attempt_1.shaders.shaders import Shaders
from scintillator_field.display.display_1.drafts.refactor_attempt_1.scintillator_blocks import ScintillatorStructure
from scintillator_field.display.display_1.drafts.refactor_attempt_1.detection_display import DetectionHulls

from scintillator_field.software.boundary_algorithm.detection_copy import Detection


class Display_1:
    def __init__(self):
        self.window = Window()
        self.appname = type(self).__name__

        self.shaders = Shaders()


        self.num_doubles = 3
        self.num_scintillators_per_structure = 2*self.num_doubles
        self.num_intra_structure_gaps_per_structure = self.num_scintillators_per_structure-1
        self.square_side_len = 120
        self.z_per_scintillator = 10
        self.space_between_scintillators = 2
        self.space_between_top_bottom = 162




    def start_time(self):
        self.dt = 0
        self.current = time.time()

        self.done = False
        self.paused = False


    def time_swaps(self):
        end = time.time()
        if end-self.current !=0:
            self.dt = end-self.current
        self.current = end


    def setup(self):
        self.window.set_window_values()




        self.window_object = self.window.build_window(self.appname)
        self.window.setup_imgui(self.window_object, self.appname)


        self.window.set_opengl_values()



        self.scintillator_structuce = ScintillatorStructure(
            num_doubles      = self.num_doubles,
            square_side_len  = self.square_side_len,
            width_per_one    = self.z_per_scintillator,
            dead_space       = self.space_between_scintillators,
            in_between_space = self.space_between_top_bottom
        )


        self.detected_hulls = DetectionHulls()
        
        self.detection_algorithm = Detection(
                num_doubles                 = self.num_doubles,
                num_scintillators           = self.num_scintillators_per_structure,
                num_intra_structure_gaps    = self.num_intra_structure_gaps_per_structure,
                square_side_len             = self.square_side_len,
                z_per_scintillator          = self.z_per_scintillator,
                space_between_scintillators = self.space_between_scintillators,
                space_between_top_bottom    = self.space_between_top_bottom,
                )
        
        
        self.shader_program = self.shaders.make_shaders()



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

        self.done = False

        self.start_time()

    




    def render_loop(self):
        self.window.begin_render_loop_actions()

        self.window.set_imgui_box_per_render(self.dt, self.paused)
        self.window.render_imgui_box()



        glUseProgram(self.shader_program)
        self.shaders.make_uniforms(self.shader_program, self.window)


        
        if self.detected_hulls.arduino.has_new_data():
            self.detected_hulls.create_hull_data(self.detection_algorithm)

        if self.detected_hulls.new_data:
            self.detected_hulls.create_hull_vao()

        self.detected_hulls.new_data = False

        if self.detected_hulls.data_exists:
            self.detected_hulls.draw_hull()
        
        
        self.scintillator_structuce.draw_scintillator_structure()


        draw_vao(self.lines_vao, GL_LINES, self.lines.shape[0])


        self.time_swaps()

        self.window.end_render_loop_actions(self.window_object)


    
    def run_window(self):
        self.setup()

        while not self.done:
            self.render_loop()
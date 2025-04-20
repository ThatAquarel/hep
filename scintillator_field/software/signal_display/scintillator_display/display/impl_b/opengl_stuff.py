from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from scintillator_display.display.impl_compatibility.camera_shader_controls import CameraShaderControls

from scintillator_display.display.impl_b.scintillator_blocks import ScintillatorStructure

from scintillator_display.display.impl_compatibility.vao_vbo import create_vao, update_vbo, draw_vao

from scintillator_display.display.impl_compatibility.xyz_axes import Axes

from scintillator_display.display.impl_compatibility.data_manager import Data

from scintillator_display.compat.pyserial_singleton import ArduinoData

class OpenGLStuff:
    def __init__(self, camera_shader:CameraShaderControls):
        # class initialisation, nothing goes here
        self.cam_shader = camera_shader


    def setup(self):
        # setup of all elements to be rendered on each loop

        self.pt_selected = None

        self.arduino = ArduinoData()

        self.data_manager = Data(impl_constant=1, impl="b",
                            hull_colour=[0.5, 0, 0.5], hull_opacity=0.8,
                            store_normals=True)
        

        self.scintillator_structure = ScintillatorStructure(self.data_manager)


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





        #if not self.data_manager.debug:
        if self.arduino.arduino_has_data(self.data_manager.debug):
            if self.data_manager.debug:
                if not self.data_manager.test_data_created:
                    self.data_manager.test_data_created = True
                    data = self.data_manager.test_data
                else:
                    data = []
            else:
                data = self.arduino.get_data_from_arduino(self.data_manager.debug)
            
            for data_point in data:
                self.data_manager.add_point(data_point)

        #elif self.data_manager.debug:
        #    if not self.data_manager.test_data_created:
        #        for data in self.data_manager.test_data:
        #            scintillator_bounds, cooked_data = self.data_manager.get_scintillator_bounds(data)
        #            if scintillator_bounds != None:
        #                self.data_manager.transform_data_per_impl(scintillator_bounds, cooked_data, data)
        #    self.data_manager.test_data_created = True

        
        self.data_manager.draw_active_hulls(self.data_manager.data, self.data_manager.impl_b_data_is_checked)



        self.scintillator_structure.reset_scintillator_colour()
        
        




        if self.pt_selected != None:
            self.scintillator_structure.recolour_for_point(self.pt_selected)



        self.scintillator_structure.renew_vbo()


        self.scintillator_structure.draw_scintillator_structure()

        if self.show_axes:
            self.xyz_axes.draw()

        pass
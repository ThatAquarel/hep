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


        self.scintillator_structuce = ScintillatorStructure(self.arduino)


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
            self.arduino.draw_active_hulls(self.arduino.data, self.arduino.impl_b_data_is_checked)




        def blend(c1,c2):
            return np.array([
                c1[0]*c1[3] + c2[0]*c2[3],
                c1[1]*c1[3] + c2[1]*c2[3],
                c1[2]*c1[3] + c2[2]*c2[3],
                (c1[3]+c2[3])/2])
        
        #print(self.scintillator_structuce.all_data.shape)
        reshaped = self.scintillator_structuce.all_data.reshape(56,12,3,10)
        #print(a.shape)


        for i, r in enumerate(reshaped):
            if i%2==0:
                arr = np.array([*self.scintillator_structuce.c1, 0.8])
                m = np.stack((arr,)*36, axis=0)
                k = m.reshape(12,3,4)
                reshaped[i, :, :, 3:7] = k

            elif i%2==1:
                arr = np.array([*self.scintillator_structuce.c2, 0.8])
                m = np.stack((arr,)*36, axis=0)
                k = m.reshape(12,3,4)
                reshaped[i, :, :, 3:7] = k




        if self.pt_selected != None:
        #if self.pt_selected == None:
            reshaped = self.scintillator_structuce.all_data.reshape(56,12,3,10)
            binary=self.arduino.num_to_raw_binary(self.pt_selected[2])

            for i, (b, r) in enumerate(zip(binary, reshaped)):
                if b == 0:
                    #print()
                    #print(reshaped[i, :, :, 3:])
                    #print(np.array([1,1,0,0.75]))
                    #print(blend(reshaped[i, :, :, 4:], np.array([1,1,0,0.75])))
                    blended = blend(reshaped[i, :, :, 3:], np.array([1,1,0,0.75]))
                    blended = np.array([1,1,0,0.75])
                    reshaped[i, 0:4, :, 3:7]  = blended
                    reshaped[i, 4:8, :, 3:7]  = blended
                    reshaped[i, 8:12, :, 3:7] = blended

                if b == 0:
                    blended = blend(reshaped[i+23, :, :, 3:], np.array([1,1,0,0.75]))
                    blended = np.array([1,1,0,0.75])
                    reshaped[i+23, 0:4, :, 3:7]  = blended
                    reshaped[i+23, 4:8, :, 3:7]  = blended
                    reshaped[i+23, 8:12, :, 3:7] = blended
                    #reshaped[i, 9:12, :, 3:] = blend(reshaped[i, :, :, 3:], np.array([1,1,0,0.75]))


        else:
            pass

        reshaped.reshape(56*12*3,10)

        update_vbo(self.scintillator_structuce.triangles_vbo, reshaped)


        self.scintillator_structuce.draw_scintillator_structure()

        if self.show_axes:
            self.xyz_axes.draw()

        pass
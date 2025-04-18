import time

import numpy as np

# from scintillator_field.display.display_1.vbo_vao_stuff import *
from scintillator_display.display.impl_b.vbo_vao_stuff import *

# from scintillator_field.software.boundary_algorithm.detection import *
from scintillator_display.math.convex_hull import ConvexHullDetection as Detection

# from scintillator_field.display.display_1.input_data import *
from scintillator_display.display.impl_ab_data_input_manager import Data


class DetectionHulls:
    def __init__(self):
        self.detection_algorithm = Detection()
        self.arduino = Data(impl_constant=1, impl="b")
        self.hull_vao = None

    
    def vec3_to_vec7(self, p_xyz, colour, opacity):
        return np.array([*p_xyz, *colour, opacity])

    def make_prism_triangles(self, p1, p2, p3, p4, p5, p6, p7, p8):

        '''
        one base has changing basepoints and x_increment of rod width
        one base has fixed basepoint and square side length increment
        z starts from box base z and add box z increment
        '''

        # front face
        tf1 = [p1, p2, p5]
        tf2 = [p2, p5, p6]

        # back face
        tb1 = [p3, p4, p7]
        tb2 = [p4, p7, p8]
        
        # left face
        tl1 = [p1, p3, p5]
        tl2 = [p3, p5, p7]

        # right face
        tr1 = [p2, p4, p6]
        tr2 = [p4, p6, p8]

        # bottom face
        tB1 = [p1, p2, p3]
        tB2 = [p2, p3, p4]

        # top face
        tT1 = [p5, p6, p7]
        tT2 = [p6, p7, p8]
        
        
        all_t = []

        all_t.extend(tf1)
        all_t.extend(tf2)
        all_t.extend(tb1)
        all_t.extend(tb2)
        all_t.extend(tl1)
        all_t.extend(tl2)
        all_t.extend(tr1)
        all_t.extend(tr2)
        #all_t.extend(tB1) # hiding these 4 faces allows for seeing through convex hull
        #all_t.extend(tB2) # hiding these 4 faces allows for seeing through convex hull
        #all_t.extend(tT1) # hiding these 4 faces allows for seeing through convex hull
        #all_t.extend(tT2) # hiding these 4 faces allows for seeing through convex hull

        return all_t


    def create_hull_data(self, hull_bounds):
        '''

        works with actual values of structure

        given:
        8 vertices bounding prism
            - coordinates on most extreme level
        sorted

        data cleaning:
        - convert coordinate systems
            - convert x, y, z, point values into local values
        - determine point order
        
        3 steps:
        - make inside prism
        - make upwards fan
        - make downwards fan

        hull_bounds = [1, 2, 3, 4, 5, 6, 7, 8]
        == [TFL, TBL, TFR, TBR, BFL, BBL, BFR, BBR]

        
        '''

        hull_colour = [0.5, 0, 0.5]
        hull_opacity = 0.8
        vec7_hull_bounds = [self.vec3_to_vec7(p, hull_colour, hull_opacity) for p in hull_bounds]

        self.hull_data = self.arduino.hull_setup_for_data_point_impl_a(vec7_hull_bounds)

        self.data_exists = True
        self.new_data = True

        return self.hull_data


    def create_hull_vao(self, data, vbo=None, vao=None):
        if vao != None:
            update_vbo_vao(data, vbo, vao)
            return vbo, vao
        else:
            vbo, vao = make_vbo_vao(data)
            return vbo, vao
    
    def draw_hull(self, vao=None, n=None):
        #draw_vao(self.hull_vao, GL_TRIANGLES, self.hull_data.shape[0])
        draw_vao(vao, GL_TRIANGLES, n)
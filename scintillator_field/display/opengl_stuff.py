from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from vbo_stuff import *


class OpenGLStuff:
    def __init__(self):
        # class initialisation, nothing goes here
        pass

    def setup(self):
        # setup of all elements to be rendered on each loop


        z_depth_per_two = 3
        num_doubles = 8
        initial_x, initial_y, initial_z = 0, 0, 0
        square_side_len = 8

        all_data = []

        for double in range(num_doubles):
            z_change = z_depth_per_two/2
            base_x, base_y, base_z = initial_x, initial_y, initial_z + double*z_depth_per_two

            num_rods = 2**(double+1)

            "xy"
            x_basepoints = np.linspace(base_x, base_x+square_side_len, num_rods, endpoint=False)
            dist_between_x_basepoints = x_basepoints[1]-x_basepoints[0]

            for rod, x in enumerate(x_basepoints):

                z_start = base_z


                colour = [1, 0, 0] if rod%2==0 else [0, 1, 0]

                p1 = np.array([x,                 base_y,                 z_start,          colour[0], colour[1], colour[2], 1]) # # BFL
                p2 = np.array([x+dist_between_x_basepoints, base_y,                 z_start,          colour[0], colour[1], colour[2], 1]) # base_point+(xlen, 0, 0) # BFR
                p3 = np.array([x,                 base_y+square_side_len, z_start,          colour[0], colour[1], colour[2], 1]) # base_point+(0, ylen, 0) # BBL
                p4 = np.array([x+dist_between_x_basepoints, base_y+square_side_len, z_start,          colour[0], colour[1], colour[2], 1]) # base_point+(xlen, ylen, 0) # BBR
                p5 = np.array([x,                 base_y,                 z_start+z_change, colour[0], colour[1], colour[2], 1]) # base_point+(0, 0, zlen) # TFL
                p6 = np.array([x+dist_between_x_basepoints, base_y,                 z_start+z_change, colour[0], colour[1], colour[2], 1]) # base_point+(xlen, 0, zlen) # TFR
                p7 = np.array([x,                 base_y+square_side_len, z_start+z_change, colour[0], colour[1], colour[2], 1]) # base_point+(0, ylen, zlen) # TBL
                p8 = np.array([x+dist_between_x_basepoints, base_y+square_side_len, z_start+z_change, colour[0], colour[1], colour[2], 1]) # base_point+(xlen, ylen, zlen) # TBR

                qf = np.array([p1, p2, p6, p5]).astype(np.float32)
                qb = np.array([p3, p4, p8, p7]).astype(np.float32)
                ql = np.array([p1, p3, p7, p5]).astype(np.float32)
                qr = np.array([p2, p4, p8, p6]).astype(np.float32)
                qB = np.array([p1, p3, p4, p2]).astype(np.float32)
                qT = np.array([p5, p7, p8, p6]).astype(np.float32)

                all_data.extend((qf, qb, ql, qr, qB, qT))


            "yx"
            y_basepoints = np.linspace(base_y, base_y+square_side_len, num_rods, endpoint=False)
            dist_between_y_basepoints = x_basepoints[1]-x_basepoints[0]


            for rod, y in enumerate(y_basepoints):

                z_start = base_z+z_depth_per_two/2
                
                colour = [1, 0, 0] if rod%2==0 else [0, 1, 0]

                p1 = np.array([base_x,                 y,                 z_start,          colour[0], colour[1], colour[2], 1]) # # BFL
                p2 = np.array([base_x+square_side_len, y,                 z_start,          colour[0], colour[1], colour[2], 1]) # base_point+(xlen, 0, 0) # BFR
                p3 = np.array([base_x,                 y+dist_between_y_basepoints, z_start,          colour[0], colour[1], colour[2], 1]) # base_point+(0, ylen, 0) # BBL
                p4 = np.array([base_x+square_side_len, y+dist_between_y_basepoints, z_start,          colour[0], colour[1], colour[2], 1]) # base_point+(xlen, ylen, 0) # BBR
                p5 = np.array([base_x,                 y,                 z_start+z_change, colour[0], colour[1], colour[2], 1]) # base_point+(0, 0, zlen) # TFL
                p6 = np.array([base_x+square_side_len, y,                 z_start+z_change, colour[0], colour[1], colour[2], 1]) # base_point+(xlen, 0, zlen) # TFR
                p7 = np.array([base_x,                 y+dist_between_y_basepoints, z_start+z_change, colour[0], colour[1], colour[2], 1]) # base_point+(0, ylen, zlen) # TBL
                p8 = np.array([base_x+square_side_len, y+dist_between_y_basepoints, z_start+z_change, colour[0], colour[1], colour[2], 1]) # base_point+(xlen, ylen, zlen) # TBR

                qf = np.array([p1, p2, p6, p5]).astype(np.float32)
                qb = np.array([p3, p4, p8, p7]).astype(np.float32)
                ql = np.array([p1, p3, p7, p5]).astype(np.float32)
                qr = np.array([p2, p4, p8, p6]).astype(np.float32)
                qB = np.array([p1, p3, p4, p2]).astype(np.float32)
                qT = np.array([p5, p7, p8, p6]).astype(np.float32)

                all_data.extend((qf, qb, ql, qr, qB, qT))

        
        all_vbo = []
        for quad in all_data:
            all_vbo.append(make_vbo(quad))

        self.all_data = np.array(all_data).astype(np.float32)
        self.all_vbo = np.array(all_vbo)


        pass

    def per_render_loop(self):
        # draw on-loop actions

        for d, v in zip(self.all_data, self.all_vbo):
            draw(d, v, GL_QUADS)

        pass
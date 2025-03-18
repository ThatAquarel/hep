from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from vbo_stuff import *


class OpenGLStuff:
    def __init__(self):
        # class initialisation, nothing goes here
        pass

    def make_quads(self, base_x, x_increment, base_y, y_increment, base_z, z_change, colour):

        '''
        one base has changing basepoints and x_increment of rod width
        one base has fixed basepoint and square side length increment
        z starts from box base z and add box z increment
        '''

        p1 = np.array([base_x,             base_y,             base_z,          colour[0], colour[1], colour[2], 1]) # base_point + (0,    0,    0)    # BFL
        p2 = np.array([base_x+x_increment, base_y,             base_z,          colour[0], colour[1], colour[2], 1]) # base_point + (xlen, 0,    0)    # BFR
        p3 = np.array([base_x,             base_y+y_increment, base_z,          colour[0], colour[1], colour[2], 1]) # base_point + (0,    ylen, 0)    # BBL
        p4 = np.array([base_x+x_increment, base_y+y_increment, base_z,          colour[0], colour[1], colour[2], 1]) # base_point + (xlen, ylen, 0)    # BBR
        p5 = np.array([base_x,             base_y,             base_z+z_change, colour[0], colour[1], colour[2], 1]) # base_point + (0,    0,    zlen) # TFL
        p6 = np.array([base_x+x_increment, base_y,             base_z+z_change, colour[0], colour[1], colour[2], 1]) # base_point + (xlen, 0,    zlen) # TFR
        p7 = np.array([base_x,             base_y+y_increment, base_z+z_change, colour[0], colour[1], colour[2], 1]) # base_point + (0,    ylen, zlen) # TBL
        p8 = np.array([base_x+x_increment, base_y+y_increment, base_z+z_change, colour[0], colour[1], colour[2], 1]) # base_point + (xlen, ylen, zlen) # TBR

        qf = np.array([p1, p2, p6, p5]).astype(np.float32) # quad front
        qb = np.array([p3, p4, p8, p7]).astype(np.float32) # quad back
        ql = np.array([p1, p3, p7, p5]).astype(np.float32) # quad left
        qr = np.array([p2, p4, p8, p6]).astype(np.float32) # quad right
        qB = np.array([p1, p3, p4, p2]).astype(np.float32) # quad bottom
        qT = np.array([p5, p7, p8, p6]).astype(np.float32) # quad top

        return (qf, qb, ql, qr, qB, qT)


    def setup(self):
        # setup of all elements to be rendered on each loop


        num_doubles = 5
        initial_x, initial_y, initial_z = 0, 0, 0
        square_side_len = 8

        width_per_one = 3
        dead_space = 2

        all_data = []

        for double in range(num_doubles):
            z_change = width_per_one
            base_x, base_y, base_z = initial_x, initial_y, initial_z + double*(2*width_per_one+2*dead_space)

            num_rods = 2**(double+1)

            "xy"
            x_basepoints = np.linspace(base_x, base_x+square_side_len, num_rods, endpoint=False)
            dist_between_x_basepoints = x_basepoints[1]-x_basepoints[0]

            for rod, x in enumerate(x_basepoints):

                z_start = base_z

                colour = [1, 0, 0] if rod%2==0 else [0, 1, 0]

                all_data.extend(
                    self.make_quads(
                        base_x      = x,                         # individual x per basepoint
                        x_increment = dist_between_x_basepoints, # rod width
                        base_y      = base_y,                    # box base y
                        y_increment = square_side_len,           # length of square
                        base_z      = z_start,                   # initial z of box
                        z_change    = z_change,                  # z depth of box
                        colour      = colour,                    # colour
                    )
                )


            "yx"
            y_basepoints = np.linspace(base_y, base_y+square_side_len, num_rods, endpoint=False)
            dist_between_y_basepoints = x_basepoints[1]-x_basepoints[0]

            for rod, y in enumerate(y_basepoints):

                z_start = base_z+width_per_one+dead_space
                
                colour = [1, 0, 0] if rod%2==0 else [0, 1, 0]

                all_data.extend(
                    self.make_quads(
                        base_x      = base_x,                    # box base x
                        x_increment = square_side_len,           # length of square
                        base_y      = y,                         # individual x per basepoint
                        y_increment = dist_between_y_basepoints, # rod width
                        base_z      = z_start,                   # initial z of box
                        z_change    = z_change,                  # z depth of box
                        colour      = colour,                    # colour
                    )
                )


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
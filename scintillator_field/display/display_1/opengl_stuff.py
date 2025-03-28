from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from vbo_vao_stuff import *
from shaders.shaders import *


class OpenGLStuff:
    def __init__(self):
        # class initialisation, nothing goes here
        pass

    def make_quads(self, base_x, x_increment, base_y, y_increment, base_z, z_change, colour, opacity):

        '''
        one base has changing basepoints and x_increment of rod width
        one base has fixed basepoint and square side length increment
        z starts from box base z and add box z increment
        '''

        p1 = np.array([base_x,             base_y,             base_z,          colour[0], colour[1], colour[2], opacity]) # base_point + (0,    0,    0)    # BFL
        p2 = np.array([base_x+x_increment, base_y,             base_z,          colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, 0,    0)    # BFR
        p3 = np.array([base_x,             base_y+y_increment, base_z,          colour[0], colour[1], colour[2], opacity]) # base_point + (0,    ylen, 0)    # BBL
        p4 = np.array([base_x+x_increment, base_y+y_increment, base_z,          colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, ylen, 0)    # BBR
        p5 = np.array([base_x,             base_y,             base_z+z_change, colour[0], colour[1], colour[2], opacity]) # base_point + (0,    0,    zlen) # TFL
        p6 = np.array([base_x+x_increment, base_y,             base_z+z_change, colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, 0,    zlen) # TFR
        p7 = np.array([base_x,             base_y+y_increment, base_z+z_change, colour[0], colour[1], colour[2], opacity]) # base_point + (0,    ylen, zlen) # TBL
        p8 = np.array([base_x+x_increment, base_y+y_increment, base_z+z_change, colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, ylen, zlen) # TBR

        # # front face
        # tf1 = np.array([p1, p2, p5]).astype(np.float32)
        # tf2 = np.array([p2, p5, p6]).astype(np.float32)
# 
        # # back face
        # tb1 = np.array([p3, p4, p7]).astype(np.float32)
        # tb2 = np.array([p4, p7, p8]).astype(np.float32)
# 
        # # left face
        # tl1 = np.array([p1, p3, p5]).astype(np.float32)
        # tl2 = np.array([p3, p5, p7]).astype(np.float32)
# 
        # # right face
        # tr1 = np.array([p2, p4, p6]).astype(np.float32)
        # tr2 = np.array([p4, p6, p8]).astype(np.float32)
# 
        # # bottom face
        # tB1 = np.array([p1, p2, p3]).astype(np.float32)
        # tB2 = np.array([p2, p3, p4]).astype(np.float32)
# 
        # # top face
        # tT1 = np.array([p5, p6, p7]).astype(np.float32)
        # tT2 = np.array([p6, p7, p8]).astype(np.float32)

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

        # quads
        #qf = np.array([p1, p2, p6, p5]).astype(np.float32) # quad front
        #qb = np.array([p3, p4, p8, p7]).astype(np.float32) # quad back
        #ql = np.array([p1, p3, p7, p5]).astype(np.float32) # quad left
        #qr = np.array([p2, p4, p8, p6]).astype(np.float32) # quad right
        #qB = np.array([p1, p3, p4, p2]).astype(np.float32) # quad bottom
        #qT = np.array([p5, p7, p8, p6]).astype(np.float32) # quad top

        all_t = []

        all_t.extend(tf1)
        all_t.extend(tf2)
        all_t.extend(tb1)
        all_t.extend(tb2)
        all_t.extend(tl1)
        all_t.extend(tl2)
        all_t.extend(tr1)
        all_t.extend(tr2)
        all_t.extend(tB1)
        all_t.extend(tB2)
        all_t.extend(tT1)
        all_t.extend(tT2)

        return all_t


    def setup(self):
        # setup of all elements to be rendered on each loop


        num_doubles = 5
        initial_x, initial_y, initial_z = 0, 0, 0
        square_side_len = 8

        width_per_one = 1
        dead_space = 1 # 2

        c1 = [1, 0.75, 0.75] # red
        c2 = [0.75, 1, 0.75] # green
        alpha = 0.8

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

                colour = c1 if rod%2==0 else c2

                all_data.extend(
                    self.make_quads(
                        base_x      = x,                         # individual x per basepoint
                        x_increment = dist_between_x_basepoints, # rod width
                        base_y      = base_y,                    # box base y
                        y_increment = square_side_len,           # length of square
                        base_z      = z_start,                   # initial z of box
                        z_change    = z_change,                  # z depth of box
                        colour      = colour,                    # colour
                        opacity     = alpha,                     # opacity
                    )
                )


            "yx"
            y_basepoints = np.linspace(base_y, base_y+square_side_len, num_rods, endpoint=False)
            dist_between_y_basepoints = x_basepoints[1]-x_basepoints[0]

            for rod, y in enumerate(y_basepoints):

                z_start = base_z+width_per_one+dead_space
                
                colour = c1 if rod%2==0 else c2

                all_data.extend(
                    self.make_quads(
                        base_x      = base_x,                    # box base x
                        x_increment = square_side_len,           # length of square
                        base_y      = y,                         # individual x per basepoint
                        y_increment = dist_between_y_basepoints, # rod width
                        base_z      = z_start,                   # initial z of box
                        z_change    = z_change,                  # z depth of box
                        colour      = colour,                    # colour
                        opacity     = alpha,                     # opacity
                    )
                )




        space_below = 8

        for double in range(num_doubles):
            z_change = width_per_one
            base_x, base_y, base_z = initial_x, initial_y, initial_z - space_below - double*(2*width_per_one+2*dead_space)

            num_rods = 2**(double+1)

            "xy"
            x_basepoints = np.linspace(base_x, base_x+square_side_len, num_rods, endpoint=False)
            dist_between_x_basepoints = x_basepoints[1]-x_basepoints[0]

            for rod, x in enumerate(x_basepoints):

                z_start = base_z

                colour = c1 if rod%2==0 else c2

                all_data.extend(
                    self.make_quads(
                        base_x      = x,                         # individual x per basepoint
                        x_increment = dist_between_x_basepoints, # rod width
                        base_y      = base_y,                    # box base y
                        y_increment = square_side_len,           # length of square
                        base_z      = z_start,                   # initial z of box
                        z_change    = z_change,                  # z depth of box
                        colour      = colour,                    # colour
                        opacity     = alpha,                     # opacity
                    )
                )


            "yx"
            y_basepoints = np.linspace(base_y, base_y+square_side_len, num_rods, endpoint=False)
            dist_between_y_basepoints = x_basepoints[1]-x_basepoints[0]

            for rod, y in enumerate(y_basepoints):

                z_start = base_z+width_per_one+dead_space
                
                colour = c1 if rod%2==0 else c2

                all_data.extend(
                    self.make_quads(
                        base_x      = base_x,                    # box base x
                        x_increment = square_side_len,           # length of square
                        base_y      = y,                         # individual x per basepoint
                        y_increment = dist_between_y_basepoints, # rod width
                        base_z      = z_start,                   # initial z of box
                        z_change    = z_change,                  # z depth of box
                        colour      = colour,                    # colour
                        opacity     = alpha,                     # opacity
                    )
                )


        #all_vbo = []
        #for quad in all_data:
        #    all_vbo.append(make_vbo(quad))

        self.all_data = np.array(all_data).astype(np.float32)
        print(self.all_data.shape)
        #self.all_vbo = np.array(all_vbo)

        self.vao = make_vao_vbo(self.all_data)[0]

        self.shader_program = make_shaders()

        pass

    def per_render_loop(self, window):
        # draw on-loop actions

        glUseProgram(self.shader_program)

        make_uniforms(self.shader_program, window)

        draw_vao(self.vao, GL_TRIANGLES, self.all_data.shape[0])

        #for d, v in zip(self.all_data, self.all_vbo):
        #    draw(d, v, GL_TRIANGLES)

        pass
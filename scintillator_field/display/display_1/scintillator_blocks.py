import numpy as np


from scintillator_field.display.display_1.vbo_vao_stuff import *


class ScintillatorStructure:
    def __init__(self):
        self.setup_structure(
                        num_doubles      =               3, # 3 each
                        x_i              =               0,
                        y_i              =               0,
                        z_i              =               0,
                        square_side_len  =               8, # 120 mm
                        width_per_one    =               1, # 9mm
                        dead_space       =               0.2, # 22 mm
                        c1               = [1, 0.75, 0.75],
                        c2               = [0.75, 1, 0.75],
                        alpha            =             0.8,
                        in_between_space =               8, # 250 mm
                        )
        self.make_vao()


    def make_prism_triangles(self, low_x, high_x, low_y, high_y, low_z, high_z, colour, opacity):
    #def make_prism_triangles(self, base_x, x_increment, base_y, y_increment, base_z, z_change, colour, opacity):

        '''
        one base has changing basepoints and x_increment of rod width
        one base has fixed basepoint and square side length increment
        z starts from box base z and add box z increment
        '''

        #p1 = np.array([base_x,             base_y,             base_z,          colour[0], colour[1], colour[2], opacity]) # base_point + (0,    0,    0)    # BFL
        #p2 = np.array([base_x+x_increment, base_y,             base_z,          colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, 0,    0)    # BFR
        #p3 = np.array([base_x,             base_y+y_increment, base_z,          colour[0], colour[1], colour[2], opacity]) # base_point + (0,    ylen, 0)    # BBL
        #p4 = np.array([base_x+x_increment, base_y+y_increment, base_z,          colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, ylen, 0)    # BBR
        #p5 = np.array([base_x,             base_y,             base_z+z_change, colour[0], colour[1], colour[2], opacity]) # base_point + (0,    0,    zlen) # TFL
        #p6 = np.array([base_x+x_increment, base_y,             base_z+z_change, colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, 0,    zlen) # TFR
        #p7 = np.array([base_x,             base_y+y_increment, base_z+z_change, colour[0], colour[1], colour[2], opacity]) # base_point + (0,    ylen, zlen) # TBL
        #p8 = np.array([base_x+x_increment, base_y+y_increment, base_z+z_change, colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, ylen, zlen) # TBR
        
        #low_x  = base_x
        #high_x = base_x+x_increment
        #low_y  = base_y
        #high_y = base_y+y_increment
        #low_z  = base_z
        #high_z = base_z+z_change

        p1 = np.array([low_x,  low_y,  low_z,  colour[0], colour[1], colour[2], opacity]) # base_point + (0,    0,    0)    # BFL
        p2 = np.array([high_x, low_y,  low_z,  colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, 0,    0)    # BFR
        p3 = np.array([low_x,  high_y, low_z,  colour[0], colour[1], colour[2], opacity]) # base_point + (0,    ylen, 0)    # BBL
        p4 = np.array([high_x, high_y, low_z,  colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, ylen, 0)    # BBR
        p5 = np.array([low_x,  low_y,  high_z, colour[0], colour[1], colour[2], opacity]) # base_point + (0,    0,    zlen) # TFL
        p6 = np.array([high_x, low_y,  high_z, colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, 0,    zlen) # TFR
        p7 = np.array([low_x,  high_y, high_z, colour[0], colour[1], colour[2], opacity]) # base_point + (0,    ylen, zlen) # TBL
        p8 = np.array([high_x, high_y, high_z, colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, ylen, zlen) # TBR


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
        all_t.extend(tB1)
        all_t.extend(tB2)
        all_t.extend(tT1)
        all_t.extend(tT2)

        return all_t

    def setup_structure(self,
                        num_doubles = 5,
                        x_i = 0, y_i = 0, z_i = 0,
                        square_side_len = 8,
                        width_per_one = 1,
                        dead_space = 0,
                        c1 = [1, 0.75, 0.75], # red
                        c2 = [0.75, 1, 0.75], # green
                        alpha = 0.8,
                        in_between_space = 8):

        
        num_doubles = num_doubles
        initial_x, initial_y, initial_z = x_i, y_i, z_i
        square_side_len = square_side_len

        width_per_one = width_per_one
        dead_space = dead_space # 0 # 2

        c1 = c1
        c2 = c2
        alpha = alpha

        all_data = []

        ''''''
        allz = []
        ''''''

        for double in range(num_doubles):
            z_change = width_per_one
            base_x, base_y, base_z = initial_x, initial_y, initial_z + double*(2*width_per_one+2*dead_space)

            num_rods = 2**(double+1)

            basepoints = np.linspace(base_x, base_x+square_side_len, num_rods, endpoint=False)
            dist_bpoints = basepoints[1]-basepoints[0]

            "xy"
            #basepoints = np.linspace(base_x, base_x+square_side_len, num_rods, endpoint=False)
            #dist_bpoints = basepoints[1]-basepoints[0]

            for rod, s in enumerate(basepoints):

                z_start = base_z

                colour = c1 if rod%2==0 else c2

                all_data.extend(
                    self.make_prism_triangles(
                        low_x=s,
                        high_x=s+dist_bpoints,
                        low_y=base_y,
                        high_y=base_y+square_side_len,
                        low_z=z_start,
                        high_z=z_start+z_change,
                        colour=colour,
                        opacity=alpha
                        )
                )

                allz.extend((z_start, z_start+z_change))


            "yx"
            #basepoints = np.linspace(base_y, base_y+square_side_len, num_rods, endpoint=False)
            #dist_bpoints = basepoints[1]-basepoints[0]

            for rod, s in enumerate(basepoints):

                z_start = base_z+width_per_one+dead_space
                
                colour = c1 if rod%2==0 else c2

                all_data.extend(
                    self.make_prism_triangles(
                        low_x=base_x,
                        high_x=base_x+square_side_len,
                        low_y=s,
                        high_y=s+dist_bpoints,
                        low_z=z_start,
                        high_z=z_start+z_change,
                        colour=colour,
                        opacity=alpha
                        )
                )
                allz.extend((z_start, z_start+z_change))





        space_below = in_between_space

        for double in range(num_doubles):
            z_change = width_per_one
            base_x, base_y, base_z = initial_x, initial_y, initial_z - space_below - double*(2*width_per_one+2*dead_space)

            num_rods = 2**(double+1)

            "xy"
            basepoints = np.linspace(base_x, base_x+square_side_len, num_rods, endpoint=False)
            dist_bpoints = basepoints[1]-basepoints[0]

            for rod, s in enumerate(basepoints):

                z_start = base_z

                colour = c1 if rod%2==0 else c2

                all_data.extend(
                    self.make_prism_triangles(
                        low_x=s,
                        high_x=s+dist_bpoints,
                        low_y=base_y,
                        high_y=base_y+square_side_len,
                        low_z=z_start,
                        high_z=z_start+z_change,
                        colour=colour,
                        opacity=alpha
                        )
                )
                allz.extend((z_start, z_start+z_change))


            "yx"
            basepoints = np.linspace(base_y, base_y+square_side_len, num_rods, endpoint=False)
            dist_bpoints = basepoints[1]-basepoints[0]

            for rod, s in enumerate(basepoints):

                z_start = base_z+width_per_one+dead_space
                
                colour = c1 if rod%2==0 else c2

                all_data.extend(
                    self.make_prism_triangles(
                        low_x=base_x,
                        high_x=base_x+square_side_len,
                        low_y=s,
                        high_y=s+dist_bpoints,
                        low_z=z_start,
                        high_z=z_start+z_change,
                        colour=colour,
                        opacity=alpha
                        )
                )
                allz.extend((z_start, z_start+z_change))

        allz = np.array([allz])
        # print(np.max(allz), np.min(allz))
        self.all_data = np.array(all_data).astype(np.float32)


    def make_vao(self):
        self.triangles_vao = make_vao_vbo(self.all_data)[0]

    def draw_scintillator_structure(self):
        draw_vao(self.triangles_vao, GL_TRIANGLES, self.all_data.shape[0])
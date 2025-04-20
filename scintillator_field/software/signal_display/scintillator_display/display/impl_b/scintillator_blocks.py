import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *


from scintillator_display.display.impl_compatibility.vao_vbo import create_vao, update_vbo, draw_vao

from scintillator_display.compat.universal_values import MathDisplayValues

from scintillator_display.display.impl_compatibility.data_manager import Data


class ScintillatorStructure(MathDisplayValues):
    def __init__(self, arduino:Data):
        self.arduino = arduino
        self.setup_structure(
                        num_doubles      =               self.NUM_SCINTILLATOR_XY_PER_STRUCTURE, # 3 each
                        x_i              =               0,
                        y_i              =               0,
                        z_i              =               0,
                        square_side_len  =               self.SQUARE_LEN, # mm
                        width_per_one    =               self.SCINTILLATOR_THICKNESS, # mm
                        dead_space       =               self.SPACE_BETWEEN_SCINTILLATORS, # mm
                        c1               = [1, 0.75, 0.75],
                        c2               = [0.75, 1, 0.75],
                        alpha            =             [0.8],
                        in_between_space =               self.SPACE_BETWEEN_STRUCTURES, # mm
                        )
        self.make_vao()


    def make_prism_triangles(self, low_x, high_x, low_y, high_y, low_z, high_z, colour=[], opacity=[]):      
        points = self.arduino.make_points_from_high_low(
            low_x, high_x, low_y, high_y, low_z, high_z, colour, opacity)

        all_t = self.arduino.make_prism_triangles(*points, show_top_bottom=True)

        return all_t

    def setup_structure(self,
                        num_doubles, x_i, y_i, z_i,
                        square_side_len, width_per_one, dead_space,
                        c1, c2, alpha, in_between_space):

        
        num_doubles = num_doubles
        initial_x, initial_y, initial_z = x_i, y_i, z_i
        square_side_len = square_side_len

        width_per_one = width_per_one
        dead_space = dead_space

        self.c1 = c1
        self.c2 = c2
        alpha = alpha

        vertices = []

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

                colour = self.c1 if rod%2==0 else self.c2

                vertices.extend(
                    self.make_prism_triangles(
                        low_x=s,
                        high_x=s+dist_bpoints,
                        low_y=base_y,
                        high_y=base_y+square_side_len,
                        low_z=z_start,
                        high_z=z_start+z_change,
                        #colour=colour,
                        #opacity=alpha
                        )
                )

                allz.extend((z_start, z_start+z_change))


            "yx"
            #basepoints = np.linspace(base_y, base_y+square_side_len, num_rods, endpoint=False)
            #dist_bpoints = basepoints[1]-basepoints[0]

            for rod, s in enumerate(basepoints):

                z_start = base_z+width_per_one+dead_space
                
                colour = self.c1 if rod%2==0 else self.c2

                vertices.extend(
                    self.make_prism_triangles(
                        low_x=base_x,
                        high_x=base_x+square_side_len,
                        low_y=s,
                        high_y=s+dist_bpoints,
                        low_z=z_start,
                        high_z=z_start+z_change,
                        #colour=colour,
                        #opacity=alpha
                        )
                )
                allz.extend((z_start, z_start+z_change))





        space_below = in_between_space

        for double in range(num_doubles):
            z_change = width_per_one
            base_x, base_y, base_z = initial_x, initial_y, initial_z - space_below - double*(2*width_per_one+2*dead_space)

            num_rods = 2**(double+1)

            "yx"
            basepoints = np.linspace(base_y, base_y+square_side_len, num_rods, endpoint=False)
            dist_bpoints = basepoints[1]-basepoints[0]

            for rod, s in enumerate(basepoints):

                z_start = base_z+width_per_one+dead_space
                
                colour = self.c1 if rod%2==0 else self.c2

                vertices.extend(
                    self.make_prism_triangles(
                        low_x=base_x,
                        high_x=base_x+square_side_len,
                        low_y=s,
                        high_y=s+dist_bpoints,
                        low_z=z_start,
                        high_z=z_start+z_change,
                        #colour=colour,
                        #opacity=alpha
                        )
                )
                allz.extend((z_start, z_start+z_change))

            "xy"
            basepoints = np.linspace(base_x, base_x+square_side_len, num_rods, endpoint=False)
            dist_bpoints = basepoints[1]-basepoints[0]

            for rod, s in enumerate(basepoints):

                z_start = base_z

                colour = self.c1 if rod%2==0 else self.c2

                vertices.extend(
                    self.make_prism_triangles(
                        low_x=s,
                        high_x=s+dist_bpoints,
                        low_y=base_y,
                        high_y=base_y+square_side_len,
                        low_z=z_start,
                        high_z=z_start+z_change,
                        #colour=colour,
                        #opacity=alpha
                        )
                )
                allz.extend((z_start, z_start+z_change))



        allz = np.array([allz])

        all_data = np.ones((len(vertices), 10), dtype=np.float32)
        all_data[:, :3] = vertices
        all_data[:, 3:6] = colour
        all_data[:, 6] = alpha
        all_data[:, 7:] = vertices

        # print(np.max(allz), np.min(allz))
        self.all_data = np.array(all_data).astype(np.float32)

    def make_vao(self):
        self.triangles_vao, self.triangles_vbo = create_vao(self.all_data, return_vbo=True, store_normals=True)

    def renew_vbo(self):
        update_vbo(self.triangles_vbo, self.reshaped)

    def draw_scintillator_structure(self):
        draw_vao(self.triangles_vao, GL_TRIANGLES, self.all_data.shape[0])

    
    def reset_scintillator_colour(self):
        
        self.reshaped = self.all_data.reshape(56,12,3,10)

        for i, r in enumerate(self.reshaped):
            if i%2==0:
                arr = np.array([*self.c1, 0.8])
                m = np.stack((arr,)*36, axis=0)
                k = m.reshape(12,3,4)
                self.reshaped[i, :, :, 3:7] = k

            elif i%2==1:
                arr = np.array([*self.c2, 0.8])
                m = np.stack((arr,)*36, axis=0)
                k = m.reshape(12,3,4)
                self.reshaped[i, :, :, 3:7] = k

        self.reshaped.reshape(56*12*3, 10)

    
    def recolour_for_point(self, point):
        binary=self.arduino.num_to_raw_binary(point[2])


        #d = {
        #    0:  [0,2,4,6],
        #    1:  [1,3,5,7],
        #    2:  [8,10,12,14],
        #    3:  [9,11,13,15],
        #    4:  [16,18],
        #    5:  [17,19],
        #    6:  [20,22],
        #    7:  [21,23],
        #    8:  [24],
        #    9:  [25],
        #    10: [26],
        #    11: [27],
        #    12: [28],
        #    13: [29],
        #    14: [30],
        #    15: [31],
        #    16: [32,34],
        #    17: [33,35],
        #    19: [36,38],
        #    18: [37,39],
        #    20: [40,42,44,46],
        #    21: [41,43,45,47],
        #    22: [48,50,52,54],
        #    23: [49,51,53,55],
        #}

        #d = {
        #    0:  [0],
        #    1:  [1],
        #    2:  [2],
        #    3:  [3],
        #    4:  [4,6],
        #    5:  [5,7],
        #    6:  [8,10],
        #    7:  [9,11],
        #    8:  [12,14,16,18],
        #    9:  [13,15,17,19],
        #    10: [20,22,24,26],
        #    11: [21,23,25,27],
        #    12: [28],
        #    13: [29],
        #    14: [30],
        #    15: [31],
        #    16: [32,34],
        #    17: [33,35],
        #    19: [36,38],
        #    18: [37,39],
        #    20: [40,42,44,46],
        #    21: [41,43,45,47],
        #    22: [48,50,52,54],
        #    23: [49,51,53,55],
        #}
        
        # top to bottom is 1 to 12
        d = {
            2:  [21, 23, 25, 27], # 1 green
            3:  [20, 22, 24, 26], # 1 red

            4:  [13, 15, 17, 19], # 2 green
            5:  [12, 14, 16, 18], # 2 red

            6:  [9, 11], # 3 green
            7:  [8, 10], # 3 red

            9:  [5, 7], # 4 green # swapped
            8:  [4, 6], # 4 red # swapped

            11: [3], # 5 green # swapped
            10: [2], # 5 red # swapped
            
            0:  [1], # 6 green
            1:  [0], # 6 red


            12: [28], # 7 red
            13: [29], # 7 green

            14: [30], # 8 red
            15: [31], # 8 green

            17: [32, 34], # 9 red # swapped
            16: [33, 35], # 9 green # swapped

            18: [36, 38], # 10 red # swapped
            19: [37, 39], # 10 green # swapped

            21: [40, 42, 44, 46], # 11 red # swapped
            20: [41, 43, 45, 47], # 11 green # swapped

            23: [48, 50, 52, 54], # 12 red # swapped
            22: [49, 51, 53, 55], # 12 green # swapped
        }


        if True:
            for i, b in enumerate(binary):
                for j in d[i]:
                    if b == 1:
                        blended = np.array([1,1,0,0.75])

                        self.reshaped[j, :4, :, 3:7]  = blended
                        self.reshaped[j, 4:8, :, 3:7]  = blended
                        self.reshaped[j, 8:12, :, 3:7] = blended


        else:
            pass

        self.reshaped.reshape(56*12*3,10)
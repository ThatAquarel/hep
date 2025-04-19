import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *


from scintillator_display.display.vao_vbo import create_vao, update_vbo, draw_vao

from scintillator_display.universal_values import MathDisplayValues

from scintillator_display.display.impl_ab_data_input_manager import Data


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


    def make_prism_triangles(self, low_x, high_x, low_y, high_y, low_z, high_z, colour, opacity):      
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
        self.triangles_vao = create_vao(self.all_data)

    def draw_scintillator_structure(self):
        draw_vao(self.triangles_vao, GL_TRIANGLES, self.all_data.shape[0])
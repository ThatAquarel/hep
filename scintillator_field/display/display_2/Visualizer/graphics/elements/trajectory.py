import numpy as np
from itertools import product
from OpenGL.GL import GL_LINES

import test
from graphics.vbo import create_vao, draw_vao, update_vbo

import random

class trajectory:
    def __init__(self, scale=1.0):
        self.scale = scale
        self.colours = self.colour()

        
    def colour(self):
        """
        Colour settings: purely cosmetic/ for visuality
        """
        r = True
        colours = []
        if r:
            for i in range(100):
                colours.append([random.randint(1,256)/256,random.randint(1,256)/256,random.randint(1,256)/256,1])
            return colours
        else:
            colours = [
            [0, 0, 0],      # Black
            [0, 1, 0],      # Green
            [1, 0, 0],      # Red
            [0, 0, 1],      # Blue
            [1, 1, 0],      # Yellow
            [1, 0, 1],      # Magenta
            [0, 1, 1],      # Cyan
            [0.5, 0, 0],    # Dark Red
            [0, 0.5, 0],    # Dark Green
            [0, 0, 0.5],    # Dark Blue
            [1, 0.5, 0],    # Orange
            [0.5, 0, 1],    # Purple
            [0, 0.5, 1],    # Sky Blue
            [0.5, 1, 0],    # Lime Green
            [1, 0, 0.5],    # Hot Pink
        ]
            return colours


    def manage_data(self, dataset_num):
        #get position for vertices
        vertices = self.interpret_data(test.data[dataset_num])
        
        self.n = len(vertices)

        # Preallocate data buffer for position, color, and normals
        self.data = np.ones((len(vertices), 10), dtype=np.float32)
        self.data[:, :3] = vertices  # Position

        #colour
        if dataset_num >= len(self.colours):
            colour_num = dataset_num % len(self.colours)
        else:
            colour_num = dataset_num

        self.data[:, 3:7] = self.colours[colour_num]

        #Set normals
        self.data[:, 7:10
        ] = vertices  

        # Build VAO and VBO
        self.vao, self.vbo = create_vao(self.data, return_vbo=True, store_normals=True)

    def interpret_data(self,data):
        '''
        Turn the x,y coordinates from the test.data into render coordinates
        :param data: (x,y) coords from binary
        :return: the coordinates (of triangles) to be rendered
        '''
        number_of_lines = self.scale / 256
        z = 0.01
        coords = []
        for i in range(len(data)-1):
            posx1 = (data[i][0]+0.5) * number_of_lines
            posy1 = (data[i][1]+0.5) * number_of_lines
            posx2 = (data[i+1][0]+0.5) * number_of_lines
            posy2 = (data[i+1][1]+0.5) * number_of_lines

            coords.append([posx1,posy1,z])
            coords.append([posx2,posy2,z])

            
        coords = np.array(coords, dtype = np.float32)
                
        return coords

    def _draw_line(self):
        """
        Draw lines for each render coordinate generated
        """
        data = np.copy(self.data)
        update_vbo(self.vbo, data)
        draw_vao(self.vao, GL_LINES, self.n)


    def draw(self, dataset_active):
        """
        Draw multiple trajectories
        """
        for i in range(len(dataset_active)):
            if dataset_active[i]:
                self.manage_data(i)
                self._draw_line()
            

                

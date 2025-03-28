import numpy as np
from itertools import product
from OpenGL.GL import GL_TRIANGLES

import test
from graphics.vbo import create_vao, draw_vao, update_vbo



class square:
    def __init__(self, scale=1.0):
        self.scale = scale
        
    def manage_data(self,dataset_num):
        vertices = self.interpret_data(test.data[dataset_num])
        
        self.n = len(vertices)

        # Preallocate data buffer for position, color, and normals
        self.data = np.ones((len(vertices), 9), dtype=np.float32)
        self.data[:, :3] = vertices  # Position

        #colour
        self.data[:, 3:6] = [1,0,0]
        self.data[0:6, 3:6] = [0,1,0]  
        self.data[-6:-1, 3:6] = [0,0,1]
        self.data[-1, 3:6] = [0,0,1]

        # Normals (approximated)
        self.data[:, 6:9] = vertices  

        # Build VAO and VBO
        self.vao, self.vbo = create_vao(self.data, return_vbo=True, store_normals=True)

    def interpret_data(self,data):
        """
        Turn data into coordinates to be rendered
        """
        number_of_lines = self.scale / 256
        z = 0.01
        coords = []
        for pt in data:
            posx1 = pt[0] * number_of_lines
            posy1 = pt[1] * number_of_lines

            posx2 = (pt[0]+1) * number_of_lines
            posy2 = pt[1] * number_of_lines
            
            posx3 = (pt[0]+1) * number_of_lines
            posy3 = (pt[1]+1) * number_of_lines

            posx4 = pt[0] * number_of_lines
            posy4 = (pt[1]+1) * number_of_lines

            #triangle 1
            coords.append([posx1,posy1,z])    
            coords.append([posx2,posy2,z])
            coords.append([posx3,posy3,z])

            coords.append([posx1,posy1,z])
            coords.append([posx3,posy3,z])
            coords.append([posx4,posy4,z])
            
        coords = np.array(coords, dtype = np.float32)
                
        return coords

    def _draw_square(self):
        """
        Draw a square
        """
        data = np.copy(self.data)
        update_vbo(self.vbo, data)
        draw_vao(self.vao, GL_TRIANGLES, self.n)


    def draw(self,dataset_active):
        """
        Draw multiple squares for multiple sets of data
        """
        
        for i in range(len(dataset_active)):
            if dataset_active[i]:
                self.manage_data(i)
                self._draw_square()

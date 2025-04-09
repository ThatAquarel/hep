import numpy as np
from itertools import product
from OpenGL.GL import GL_TRIANGLES

from graphics.vbo import create_vao, draw_vao, update_vbo



class square:
    def __init__(self, scale=1.0):
        self.scale = scale
        self.input_data = []
        
    def manage_data(self,dataset_num):
        #vertices = self.interpret_data(test.data[dataset_num])

        vertices = self.interpret_data(self.input_data[dataset_num])
        
        self.n = len(vertices)

        # Preallocate data buffer for position, color, and normals
        self.data = np.ones((len(vertices), 10), dtype=np.float32)
        self.data[:, :3] = vertices  # Position

        #colour
        self.data[:, 3:7] = [1,0,0,0.3]
        # self.data[0:36, 3:7] = [0,1,0,1]  
        # self.data[-36:-1, 3:7] = [0,0,1,1]
        # self.data[-1, 3:7] = [0,0,1,1]

        # Normals (approximated)
        self.data[:, 7:10] = vertices  

        # Build VAO and VBO
        self.vao, self.vbo = create_vao(self.data, return_vbo=True, store_normals=True)

    # def interpret_data(self,data):
    #     """
    #     Turn data into coordinates to be rendered
    #     """
    #     number_of_lines = self.scale / 256
    #     z = 0.01
    #     coords = []
    #     for pt in data:
    #         posx1 = pt[0] * number_of_lines
    #         posy1 = pt[1] * number_of_lines

    #         posx2 = (pt[0]+1) * number_of_lines
    #         posy2 = pt[1] * number_of_lines
            
    #         posx3 = (pt[0]+1) * number_of_lines
    #         posy3 = (pt[1]+1) * number_of_lines

    #         posx4 = pt[0] * number_of_lines
    #         posy4 = (pt[1]+1) * number_of_lines

    #         #triangle 1
    #         coords.append([posx1,posy1,z])    
    #         coords.append([posx2,posy2,z])
    #         coords.append([posx3,posy3,z])

    #         coords.append([posx1,posy1,z])
    #         coords.append([posx3,posy3,z])
    #         coords.append([posx4,posy4,z])
            
    #     coords = np.array(coords, dtype = np.float32)
                
    #     return coords

    def interpret_data(self,data):
        vertices = []
        for cube in data:


            p1 = cube[0][0]
            p2 = cube[0][1]
            p3 = cube[0][2]
            p4 = cube[0][3]
            p5 = cube[0][4]
            p6 = cube[0][5]
            p7 = cube[0][6]
            p8 = cube[0][7]

            # Front face
            vertices.append(p5)
            vertices.append(p1)
            vertices.append(p7)
            vertices.append(p1)
            vertices.append(p7)
            vertices.append(p3)
            # Back face
            vertices.append(p6)
            vertices.append(p2)
            vertices.append(p8)
            vertices.append(p2)
            vertices.append(p8)
            vertices.append(p4)
            # Left face
            vertices.append(p5)
            vertices.append(p1)
            vertices.append(p6)
            vertices.append(p1)
            vertices.append(p6)
            vertices.append(p2)
            # Right face
            vertices.append(p7)
            vertices.append(p3)
            vertices.append(p8)
            vertices.append(p3)
            vertices.append(p8)
            vertices.append(p4)

        vertices = np.array(vertices, dtype = np.float32)
        return vertices

    def _draw_square(self):
        """
        Draw a square
        """

        update_vbo(self.vbo, self.data)
        draw_vao(self.vao, GL_TRIANGLES, self.n)


    def draw(self,dataset_active):
        """
        Draw multiple squares for multiple sets of data
        """
        if self.input_data == []:
            return
        else:
            for i in range(len(dataset_active)):
                if dataset_active[i]:
                    self.manage_data(i)
                    self._draw_square()

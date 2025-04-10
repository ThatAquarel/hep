import numpy as np
from itertools import product
from OpenGL.GL import GL_TRIANGLES

from graphics.vbo import create_vao, draw_vao, update_vbo



class Fan:
    def __init__(self, scale=1.0):
        self.scale = scale
        self.input_data = []
        
    def manage_data(self,prism):
        """
        manage data
        """
        #vertices = self.interpret_data(test.data[dataset_num])

        vertices = self.interpret_data(prism)
        
        self.n = len(vertices)

        # Preallocate data buffer for position, color, and normals
        self.data = np.ones((len(vertices), 10), dtype=np.float32)
        self.data[:, :3] = vertices  # Position

        #colour
        self.data[:, 3:7] = [1,0,0,0.3]
        # self.data[0:72, 3:7] = [0,1,0,1]  
        # self.data[-72:-1, 3:7] = [0,0,1,1]
        # self.data[-1, 3:7] = [0,0,1,1]

        # Normals (approximated)
        self.data[:, 7:10] = vertices  

        # Build VAO and VBO
        self.vao, self.vbo = create_vao(self.data, return_vbo=True, store_normals=True)

    def fanned_coords(self,pair):
        """
        transform the given coordinates into coordinates to be drawn
        """
        scale = 3
        z_scale = 128
        dx = (pair[0][0] - pair[1][0]) * scale
        dy = (pair[0][1] - pair[1][1]) * scale
        dz = (pair[0][2] - pair[1][2]) * scale

        return [pair[0][0] + dx, pair[0][1] + dy, (pair[0][2] + dz)]

    def interpret_data(self,prism):
        """
        Create veritex datas
        """
        vertices = []

        p1 = self.fanned_coords(prism[1][0])
        p2 = self.fanned_coords(prism[1][1])
        p3 = self.fanned_coords(prism[1][2])
        p4 = self.fanned_coords(prism[1][3])

        #tuple to list
        
        p5 = [prism[0][0][0],prism[0][0][1],prism[0][0][2]]
        p6 = [prism[0][1][0],prism[0][1][1],prism[0][1][2]]
        p7 = [prism[0][2][0],prism[0][2][1],prism[0][2][2]]
        p8 = [prism[0][3][0],prism[0][3][1],prism[0][3][2]]
        
        

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

        # # Top face
        # vertices.append(p1)
        # vertices.append(p2)
        # vertices.append(p3)
        # vertices.append(p2)
        # vertices.append(p3)
        # vertices.append(p4)
        # # Bottom face
        # vertices.append(p5)
        # vertices.append(p6)
        # vertices.append(p7)
        # vertices.append(p6)
        # vertices.append(p7)
        # vertices.append(p8)
        
        
        #coords
        p1 = [prism[0][4][0],prism[0][4][1],prism[0][4][2]]
        p2 = [prism[0][5][0],prism[0][5][1],prism[0][5][2]]
        p3 = [prism[0][6][0],prism[0][6][1],prism[0][6][2]]
        p4 = [prism[0][7][0],prism[0][7][1],prism[0][7][2]]


        #tuple to list
        p5 = self.fanned_coords((prism[1][3][1],prism[1][3][0]))
        p6 = self.fanned_coords((prism[1][2][1],prism[1][2][0]))
        p7 = self.fanned_coords((prism[1][1][1],prism[1][1][0]))
        p8 = self.fanned_coords((prism[1][0][1],prism[1][0][0]))

        
        # #scale z
        # p1[2] = p1[2]/128
        # p2[2] = p2[2]/128
        # p3[2] = p3[2]/128
        # p4[2] = p4[2]/128
        

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

        # # Top face
        # vertices.append(p1)
        # vertices.append(p2)
        # vertices.append(p3)
        # vertices.append(p2)
        # vertices.append(p3)
        # vertices.append(p4)
        # # Bottom face
        # vertices.append(p5)
        # vertices.append(p6)
        # vertices.append(p7)
        # vertices.append(p6)
        # vertices.append(p7)
        # vertices.append(p8)

        vertices = np.array(vertices, dtype = np.float32)


        return vertices


    def _draw_square(self):
        """
        Draw a square
        """
        update_vbo(self.vbo, self.data)
        draw_vao(self.vao, GL_TRIANGLES, self.n)


    def draw(self,input_data, dataset_active):
        """
        Draw multiple squares for multiple sets of data
        """
        if input_data == []:
            return
        else:
            for i in range(len(dataset_active)):
                if dataset_active != [] and input_data != []:
                    if dataset_active[i]:
                        self.manage_data(input_data[i])
                        self._draw_square()

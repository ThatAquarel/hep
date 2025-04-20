import numpy as np
from itertools import product
from OpenGL.GL import GL_TRIANGLES

from graphics.vbo import create_vao, draw_vao, update_vbo



class square:
    def __init__(self, scale=1.0):
        self.scale = scale
        self.input_data = []
        
    def manage_data(self,prism):
        """
        manage data
        """

        vertices = self.interpret_data(prism)
        
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


    def interpret_data(self,prism):
        """
        Create veritex datas
        """
        vertices = []


        p1 = prism[0][0]
        p2 = prism[0][1]
        p3 = prism[0][2]
        p4 = prism[0][3]
        p5 = prism[0][4]
        p6 = prism[0][5]
        p7 = prism[0][6]
        p8 = prism[0][7]

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

    def _draw_prism(self):
        """
        Draw a prism
        """

        update_vbo(self.vbo, self.data)
        draw_vao(self.vao, GL_TRIANGLES, self.n)


    def draw(self,input_data, dataset_active):
        """
        Draw multiple prisms for multiple sets of data
        """
        if input_data == []:
            return
        else:
            for i in range(len(input_data)):

                if dataset_active != [] and input_data != []:    #check if there's any data 
                    if dataset_active[i]:
                        self.manage_data(input_data[i])
                        self._draw_prism()

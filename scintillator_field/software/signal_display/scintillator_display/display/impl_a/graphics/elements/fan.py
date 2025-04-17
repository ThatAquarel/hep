import numpy as np
from itertools import product
from OpenGL.GL import GL_TRIANGLES

from scintillator_display.display.impl_a.graphics.vbo import create_vao, draw_vao, update_vbo



class Fan:
    def __init__(self, arduino_data_manager, scale=1.0):
        self.scale = scale
        self.input_data = []
        self.arduino_data_manager = arduino_data_manager
        
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


    def interpret_data(self,prism):
        """
        Create veritex datas
        """
        vertices = []

        hull_bounds = prism[0]
        scaled_hull_bounds = self.arduino_data_manager.scale_hull_bounds(hull_bounds)

        p1 = scaled_hull_bounds[0]
        p2 = scaled_hull_bounds[1]
        p3 = scaled_hull_bounds[2]
        p4 = scaled_hull_bounds[3]

        p5 = hull_bounds[0]
        p6 = hull_bounds[1]
        p7 = hull_bounds[2]
        p8 = hull_bounds[3]     
        
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
        



        p1 = hull_bounds[4]
        p2 = hull_bounds[5]
        p3 = hull_bounds[6]
        p4 = hull_bounds[7]


        p5 = scaled_hull_bounds[4]
        p6 = scaled_hull_bounds[5]
        p7 = scaled_hull_bounds[6]
        p8 = scaled_hull_bounds[7]
        

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

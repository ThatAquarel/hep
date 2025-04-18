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
        
        vertices = self.arduino_data_manager.hull_setup_for_data_point_impl_a(prism[0])
        
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

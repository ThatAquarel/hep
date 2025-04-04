import numpy as np
from itertools import product
from OpenGL.GL import GL_TRIANGLES

import test
from graphics.vbo import create_vao, draw_vao, update_vbo



class Fan:
    def __init__(self, scale=1.0):
        self.scale = scale
        
    def manage_data(self,dataset_num):
        #vertices = self.interpret_data(test.data[dataset_num])

        vertices = self.interpret_data(test.data[dataset_num])
        
        self.n = len(vertices)

        # Preallocate data buffer for position, color, and normals
        self.data = np.ones((len(vertices), 10), dtype=np.float32)
        self.data[:, :3] = vertices  # Position

        #colour
        self.data[:, 3:7] = [1,0,0,1]

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

    def fanned_coords(self,pair):
        scale = 1
        dx = (pair[0][0] - pair[1][0]) * scale
        dy = (pair[0][1] - pair[1][1]) * scale
        dz = (pair[0][2] - pair[1][2]) * scale

        return [pair[0][0] + dx, pair[0][1] + dy, (pair[0][2] + dz)/128]

    def interpret_data(self,data):
        vertices = []

        for cube in data:
            p1 = self.fanned_coords(cube[1][0])
            p2 = self.fanned_coords(cube[1][1])
            p3 = self.fanned_coords(cube[1][2])
            p4 = self.fanned_coords(cube[1][3])

            #tuple to list
            
            p5 = [cube[0][0][0],cube[0][0][1],cube[0][0][2]]
            p6 = [cube[0][1][0],cube[0][1][1],cube[0][1][2]]
            p7 = [cube[0][2][0],cube[0][2][1],cube[0][2][2]]
            p8 = [cube[0][3][0],cube[0][3][1],cube[0][3][2]]
            
            #scale z
            p5[2] = p5[2]/128
            p6[2] = p6[2]/128
            p7[2] = p7[2]/128
            p8[2] = p8[2]/128
            

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
            p1 = [cube[0][4][0],cube[0][4][1],cube[0][4][2]]
            p2 = [cube[0][5][0],cube[0][5][1],cube[0][5][2]]
            p3 = [cube[0][6][0],cube[0][6][1],cube[0][6][2]]
            p4 = [cube[0][7][0],cube[0][7][1],cube[0][7][2]]


            #tuple to list
            p5 = self.fanned_coords((cube[1][3][1],cube[1][3][0]))
            p6 = self.fanned_coords((cube[1][2][1],cube[1][2][0]))
            p7 = self.fanned_coords((cube[1][1][1],cube[1][1][0]))
            p8 = self.fanned_coords((cube[1][0][1],cube[1][0][0]))

            
            #scale z
            p1[2] = p1[2]/128
            p2[2] = p2[2]/128
            p3[2] = p3[2]/128
            p4[2] = p4[2]/128
            

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


    def draw(self,dataset_active):
        """
        Draw multiple squares for multiple sets of data
        """
        
        for i in range(len(dataset_active)):
            if dataset_active[i]:
                self.manage_data(i)
                self._draw_square()

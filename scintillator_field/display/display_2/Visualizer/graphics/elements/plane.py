import numpy as np
from itertools import product
from OpenGL.GL import GL_TRIANGLES

from graphics.vbo import create_vao, draw_vao, update_vbo



class Plane:
    def __init__(self, scale=1.0):

        self.scale = scale

        self.number_of_layers = 6
        
        #generate the vertices
        self.vertices = self.generate_plane_vertices(self.scale)
        self.n = len(self.vertices)
        
        # Preallocate data buffer for position, color, and normals
        self.data = np.ones((len(self.vertices), 10), dtype=np.float32)

        #Set Positions
        self.data[:, :3] = self.vertices 

        # #Set colour
        for i in range(len(self.vertices)):
            if i %2 ==  0 :
                self.data[i*36:(i+1)*36,3:7] = [1,1,1,0.5]  #white
                #self.data[i*36:(i+1)*36,3:7] = [1,0,0,0.5] 
            else:
                self.data[i*36:(i+1)*36,3:7] = [211/256,211/256,211/256,0.5]   #gray
                #self.data[i*36:(i+1)*36,3:7] = [0,1,0,0.5]


        #Set normals
        self.data[:, 7:10] = self.vertices  
        
        # Build VAO and VBO
        self.vao, self.vbo = create_vao(self.data, return_vbo=True, store_normals=True)

    def generate_plane_vertices(self,size):
        """
        Generate vertices for the plane
        """

        #size = 2
        unit = size / 2
        
        vertices = []

        offset = 0.4

        z_ratio = 0.1

        layer_gap = size * z_ratio

        #Lower plane
        for layer in range(2,2+self.number_of_layers):
            number_of_strips = 2** (layer//2)

            strip_length = size / number_of_strips
            z1 = (layer) * size * -z_ratio +  offset - layer_gap * (layer - 2) #z
            z2 = (layer + 1) * size * -z_ratio  + offset - layer_gap * (layer - 2)        #-z

            for i in range(number_of_strips):
                if layer % 2 == 1:   #axis = y
                    x1 = -unit       #s
                    x2 = unit      #-s
                    y1 = -unit + (i+1) * strip_length       #-s
                    y2 = -unit + (i) * strip_length      #s        #-z
                    
                else: #axis = x
                    x1 = -unit + (i+1) * strip_length       #s
                    x2 = -unit + i * strip_length       #-s
                    y1 = -unit      #-s
                    y2 = unit    #s
                    
                # Front face
                vertices.append([x2, y1, z1])
                vertices.append([x1, y1, z1])
                vertices.append([x1, y2, z1])
                vertices.append([x2, y1, z1])
                vertices.append([x1, y2, z1])
                vertices.append([x2, y2, z1])
                # Back face
                vertices.append([x2, y1, z2])
                vertices.append([x2, y2, z2])
                vertices.append([x1, y2, z2])
                vertices.append([x2, y1, z2])
                vertices.append([x1, y2, z2])
                vertices.append([x1, y1, z2])
                # Left face
                vertices.append([x2, y1, z2])
                vertices.append([x2, y1, z1])
                vertices.append([x2, y2, z1])
                vertices.append([x2, y1, z2])
                vertices.append([x2, y2, z1])
                vertices.append([x2, y2, z2])
                # Right face
                vertices.append([x1, y1, z2])
                vertices.append([x1, y2, z2])
                vertices.append([x1, y2, z1])
                vertices.append([x1, y1, z2])
                vertices.append([x1, y2, z1])
                vertices.append([x1, y1, z1])
                # Top face
                vertices.append([x2, y2, z2])
                vertices.append([x2, y2, z1])
                vertices.append([x1, y2, z1])
                vertices.append([x2, y2, z2])
                vertices.append([x1, y2, z1])
                vertices.append([x1, y2, z2])
                # Bottom face
                vertices.append([x2, y1, z2])
                vertices.append([x1, y1, z2])
                vertices.append([x1, y1, z1])
                vertices.append([x2, y1, z2])
                vertices.append([x1, y1, z1])
                vertices.append([x2, y1, z1])

        #vertices = np.array(vertices, dtype = np.float32)

        #Up plane
        middle_gap = 1
        for layer in range(2,2+self.number_of_layers):
            number_of_strips = 2** (layer//2)

            strip_length = size / number_of_strips
            z1 = layer * size * z_ratio - offset + middle_gap + layer_gap * (layer - 2)      #z
            z2 = (layer + 1) * size * z_ratio  - offset + middle_gap + layer_gap * (layer - 2)       #-z

            for i in range(number_of_strips):
                if layer % 2 == 0:   #axis = x
                    x1 = -unit       #s
                    x2 = unit      #-s
                    y1 = -unit + (i+1) * strip_length       #-s
                    y2 = -unit + (i) * strip_length      #s        #-z
                    
                else: #axis = x
                    x1 = -unit + (i+1) * strip_length       #s
                    x2 = -unit + i * strip_length       #-s
                    y1 = -unit      #-s
                    y2 = unit    #s
                    
                # Front face
                vertices.append([x2, y1, z1])
                vertices.append([x1, y1, z1])
                vertices.append([x1, y2, z1])
                vertices.append([x2, y1, z1])
                vertices.append([x1, y2, z1])
                vertices.append([x2, y2, z1])
                # Back face
                vertices.append([x2, y1, z2])
                vertices.append([x2, y2, z2])
                vertices.append([x1, y2, z2])
                vertices.append([x2, y1, z2])
                vertices.append([x1, y2, z2])
                vertices.append([x1, y1, z2])
                # Left face
                vertices.append([x2, y1, z2])
                vertices.append([x2, y1, z1])
                vertices.append([x2, y2, z1])
                vertices.append([x2, y1, z2])
                vertices.append([x2, y2, z1])
                vertices.append([x2, y2, z2])
                # Right face
                vertices.append([x1, y1, z2])
                vertices.append([x1, y2, z2])
                vertices.append([x1, y2, z1])
                vertices.append([x1, y1, z2])
                vertices.append([x1, y2, z1])
                vertices.append([x1, y1, z1])
                # Top face
                vertices.append([x2, y2, z2])
                vertices.append([x2, y2, z1])
                vertices.append([x1, y2, z1])
                vertices.append([x2, y2, z2])
                vertices.append([x1, y2, z1])
                vertices.append([x1, y2, z2])
                # Bottom face
                vertices.append([x2, y1, z2])
                vertices.append([x1, y1, z2])
                vertices.append([x1, y1, z1])
                vertices.append([x2, y1, z2])
                vertices.append([x1, y1, z1])
                vertices.append([x2, y1, z1])

        vertices = np.array(vertices, dtype = np.float32)

        return vertices
    
    def set_colour(self, pt_selected):
        if pt_selected == None:
            x = -1
            y = -1
        else:

        
        #In here 111111 means that all of the positives light up(more towards positive x or y)
        #000000 means that all of the negative(more towards the negative x or y)

        #More towards the positive has a white strip, more towards the negative has a gray strip
            for up_or_top in range(2):  #ensures that both top and up layer are set
                if up_or_top == 0:
                    x = (pt_selected[2] & 3584) >> 9
                    y = (pt_selected[2] & 56) >> 3
                else:
                    x = (pt_selected[2] &448) >> 6
                    y = pt_selected[2] & 7
                    

                for layer in range(self.number_of_layers):
                    number_of_strips = 2 ** ((layer + 2)//2)    #calculate the number of strips per layer


                    for i in range(number_of_strips):
                        reverse_number = 2** ((5-layer)//2)    #This means that the binary is read from left to right

                        k = 0 + 28 * up_or_top  #apply offset so when it comes to top, it correctly displays
                        for j in range(layer + 1):  #Find the number of the strip we are on. This is counting by 2^x
                            if j != 0:
                                k += 2**((j+1)//2)

                        k = (k + i) * 36    #+i since it is the number of the strip in that layer. 36 is for each prism has 36 vertices

                        if layer % 2 == 0:  #x - axis
                            if i % 2 == 1:  #white strips
                                if x & reverse_number != 0 and x != -1: #If x in that spot is 1
                                    
                                    self.data[k : k + 36, 3:6] = [1,1,0]    #light up
                                else: 
                                    self.data[k : k + 36, 3:6] = [1,1,1]    #default colour(white)
                            else:   #second strip (grey)
                                if x & reverse_number == 0: #If x in that spot is 0
                                    self.data[k : k + 36, 3:6] = [1,1,0]    #light up
                                else: 
                                    self.data[k : k + 36, 3:6] = [211/256,211/256,211/256]  #default colour: gray
                        else:
                            if i % 2 == 1:  #white strips
                                if y & reverse_number != 0 and y != -1: 
                                    
                                    self.data[k : k + 36, 3:6] = [1,1,0]
                                else: 
                                    self.data[k : k + 36, 3:6] = [1,1,1]
                            else: 
                                if y & reverse_number == 0: 
                                    self.data[k : k + 36, 3:6] = [1,1,0]
                                else: 
                                    self.data[k : k + 36, 3:6] = [211/256,211/256,211/256]








    def draw(self, pt_selected):
        """
        Draw the planes
        """
        
        self.set_colour(pt_selected)
        update_vbo(self.vbo, self.data)
        draw_vao(self.vao, GL_TRIANGLES, self.n)

    # def set_color(self, new_color):
    #     """
    #     Update cube color.
    #     """
    #     self.data[:, 3:6] = new_color
    #     update_vbo(self.vbo, self.data)

    # def draw(self, positions, sizes):
    #     """
    #     Draw multiple cubes.
    #     """
    #     if not len(positions):
    #         return
        
    #     for pos, size in zip(positions, sizes):
    #         self._draw_cube(size, pos)

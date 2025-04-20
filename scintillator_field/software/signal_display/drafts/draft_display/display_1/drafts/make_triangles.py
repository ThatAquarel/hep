import numpy as np


def make_triangles(self, base_x, x_increment, base_y, y_increment, base_z, z_change, colour, opacity):

        '''
        one base has changing basepoints and x_increment of rod width
        one base has fixed basepoint and square side length increment
        z starts from box base z and add box z increment
        '''

        p1 = np.array([base_x,             base_y,             base_z,          colour[0], colour[1], colour[2], opacity]) # base_point + (0,    0,    0)    # BFL
        p2 = np.array([base_x+x_increment, base_y,             base_z,          colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, 0,    0)    # BFR
        p3 = np.array([base_x,             base_y+y_increment, base_z,          colour[0], colour[1], colour[2], opacity]) # base_point + (0,    ylen, 0)    # BBL
        p4 = np.array([base_x+x_increment, base_y+y_increment, base_z,          colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, ylen, 0)    # BBR
        p5 = np.array([base_x,             base_y,             base_z+z_change, colour[0], colour[1], colour[2], opacity]) # base_point + (0,    0,    zlen) # TFL
        p6 = np.array([base_x+x_increment, base_y,             base_z+z_change, colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, 0,    zlen) # TFR
        p7 = np.array([base_x,             base_y+y_increment, base_z+z_change, colour[0], colour[1], colour[2], opacity]) # base_point + (0,    ylen, zlen) # TBL
        p8 = np.array([base_x+x_increment, base_y+y_increment, base_z+z_change, colour[0], colour[1], colour[2], opacity]) # base_point + (xlen, ylen, zlen) # TBR

        # # front face
        # tf1 = np.array([p1, p2, p5]).astype(np.float32)
        # tf2 = np.array([p2, p5, p6]).astype(np.float32)
# 
        # # back face
        # tb1 = np.array([p3, p4, p7]).astype(np.float32)
        # tb2 = np.array([p4, p7, p8]).astype(np.float32)
# 
        # # left face
        # tl1 = np.array([p1, p3, p5]).astype(np.float32)
        # tl2 = np.array([p3, p5, p7]).astype(np.float32)
# 
        # # right face
        # tr1 = np.array([p2, p4, p6]).astype(np.float32)
        # tr2 = np.array([p4, p6, p8]).astype(np.float32)
# 
        # # bottom face
        # tB1 = np.array([p1, p2, p3]).astype(np.float32)
        # tB2 = np.array([p2, p3, p4]).astype(np.float32)
# 
        # # top face
        # tT1 = np.array([p5, p6, p7]).astype(np.float32)
        # tT2 = np.array([p6, p7, p8]).astype(np.float32)

        # front face
        tf1 = [p1, p2, p5]
        tf2 = [p2, p5, p6]

        # back face
        tb1 = [p3, p4, p7]
        tb2 = [p4, p7, p8]
        
        # left face
        tl1 = [p1, p3, p5]
        tl2 = [p3, p5, p7]

        # right face
        tr1 = [p2, p4, p6]
        tr2 = [p4, p6, p8]

        # bottom face
        tB1 = [p1, p2, p3]
        tB2 = [p2, p3, p4]

        # top face
        tT1 = [p5, p6, p7]
        tT2 = [p6, p7, p8]

        # quads
        #qf = np.array([p1, p2, p6, p5]).astype(np.float32) # quad front
        #qb = np.array([p3, p4, p8, p7]).astype(np.float32) # quad back
        #ql = np.array([p1, p3, p7, p5]).astype(np.float32) # quad left
        #qr = np.array([p2, p4, p8, p6]).astype(np.float32) # quad right
        #qB = np.array([p1, p3, p4, p2]).astype(np.float32) # quad bottom
        #qT = np.array([p5, p7, p8, p6]).astype(np.float32) # quad top

        all_t = []

        all_t.extend(tf1)
        all_t.extend(tf2)
        all_t.extend(tb1)
        all_t.extend(tb2)
        all_t.extend(tl1)
        all_t.extend(tl2)
        all_t.extend(tr1)
        all_t.extend(tr2)
        all_t.extend(tB1)
        all_t.extend(tB2)
        all_t.extend(tT1)
        all_t.extend(tT2)

        return all_t
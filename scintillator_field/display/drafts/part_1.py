"""

from opengl_stuff
testing for making 3D structure

"""



#
        #'''
        #take base point, num on level, len, width
        #calculate points per rod
        #make flat quads per rod
        #make long outside quads
        #'''
#
#
        #p_all = []
#
#
        #bx, by, bz = (0,)*3
        #total_x, total_y, zlen = 4, 9, 2
        #num_rods = 2**(0+1)
        ## for direction = x
        #endpoints = np.linspace(bx, bx+total_x, num_rods+1, endpoint=True)
        ##print(endpoints)
#
        #x_pairs = []
        #for i, j in zip(endpoints[:-1], endpoints[1:]):
        #    x_pairs.append((i, j))
#
        #p_in_iter = 0
        ##p_all = []
        #for xpair in x_pairs:
        #    c1, c2, c3 = (1, 0, 0) if p_in_iter%2==0 else (0, 1, 0)
        #    p1 = np.array([xpair[0], by,         bz, c1, c2, c3, 1])
        #    p2 = np.array([xpair[0], by+total_y, bz, c1, c2, c3, 1])
        #    p3 = np.array([xpair[1], by+total_y, bz, c1, c2, c3, 1])
        #    p4 = np.array([xpair[1], by,         bz, c1, c2, c3, 1])
        #    px = np.array([p1, p2, p3, p4])
        #    p_in_iter += 1
        #    p_all.append(px)
    #
        #self.t1_d = np.array(p_all).astype(np.float32)
        #self.t1_v = np.array([make_vbo(r) for r in self.t1_d])
#
#
#
#
#




#
#
#
#
        #r = [1, 0, 0]
        #g = [0, 1, 0]
#
#
        #sqbx, sqby, sqbz = (2, 2, 2)
        #square_len = 5
        #n = 1
        #num_rods = 2**(n+1)
        #x_startpoints = np.linspace(sqbx, sqbx+square_len, num_rods+1, endpoint=False)
        ##print(x_startpoints)
#
        #q_all = []
        #v_all = []
#
#
#
        #xlen, ylen, zlen = (square_len/(num_rods+1), square_len, 0.5)
#
        #for k in range(2):
#
#
#
        #    for i, x in enumerate(x_startpoints):
#
        #        xb, yb, zb = x, sqby, sqbz
        #        if k==1:
        #            zb+=zlen
        #            a=xlen
        #            b=ylen
        #            xlen=b
        #            ylen=a
        #        
        #        c = r if i%2==0 else g
#
        #        p1 = np.array([xb,      yb     , zb,      c[0], c[1], c[2], 1]) # # BFL
        #        p2 = np.array([xb+xlen, yb     , zb,      c[0], c[1], c[2], 1]) # base_point+(xlen, 0, 0) # BFR
        #        p3 = np.array([xb,      yb+ylen, zb,      c[0], c[1], c[2], 1]) # base_point+(0, ylen, 0) # BBL
        #        p4 = np.array([xb+xlen, yb+ylen, zb,      c[0], c[1], c[2], 1]) # base_point+(xlen, ylen, 0) # BBR
        #        p5 = np.array([xb,      yb     , zb+zlen, c[0], c[1], c[2], 1]) # base_point+(0, 0, zlen) # TFL
        #        p6 = np.array([xb+xlen, yb     , zb+zlen, c[0], c[1], c[2], 1]) # base_point+(xlen, 0, zlen) # TFR
        #        p7 = np.array([xb,      yb+ylen, zb+zlen, c[0], c[1], c[2], 1]) # base_point+(0, ylen, zlen) # TBL
        #        p8 = np.array([xb+xlen, yb+ylen, zb+zlen, c[0], c[1], c[2], 1]) # base_point+(xlen, ylen, zlen) # TBR
#
        #        
#
#
        #        qf = np.array([p1, p2, p6, p5]).astype(np.float32)
        #        qb = np.array([p3, p4, p8, p7]).astype(np.float32)
        #        ql = np.array([p1, p3, p7, p5]).astype(np.float32)
        #        qr = np.array([p2, p4, p8, p6]).astype(np.float32)
        #        qB = np.array([p1, p3, p4, p2]).astype(np.float32)
        #        qT = np.array([p5, p7, p8, p6]).astype(np.float32)
#
#
#
#
#
        #        q_all.extend((qf, qb, ql, qr, qB, qT))
#
        #self.q = q_all
        #v = []
        #for q in self.q:
        #    v.append(make_vbo(q))
        #self.v = np.array(v)


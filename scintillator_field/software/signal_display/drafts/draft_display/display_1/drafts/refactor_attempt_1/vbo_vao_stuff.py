from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


def make_vao_vbo(data):
    n_per_vertice = 3
    n_per_colour = 3
    n_opacity = 1
    data_items_per_point = len(data[0])
    data_stride = data_items_per_point*data.itemsize

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, n_per_vertice, GL_FLOAT, GL_FALSE, data_stride, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, n_per_colour, GL_FLOAT, GL_FALSE, data_stride, ctypes.c_void_p(n_per_vertice * data.itemsize))
    
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, n_opacity, GL_FLOAT, GL_FALSE, data_stride, ctypes.c_void_p((n_per_vertice+n_per_colour) * data.itemsize))
    
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao, vbo


def update_vao_vbo(data, vao, vbo):
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    glBufferSubData(GL_ARRAY_BUFFER, 0, data.nbytes, data)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)


def draw_vao(vao, draw_type, n):
    glBindVertexArray(vao)
    glPointSize(10)
    glLineWidth(15)
    glDrawArrays(draw_type, 0, n)
    glBindVertexArray(0)
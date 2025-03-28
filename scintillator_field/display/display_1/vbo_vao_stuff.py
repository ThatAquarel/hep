from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


def make_vao_vbo(data):
    n_per_vertice = 3
    n_per_colour = 4
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
    glDrawArrays(draw_type, 0, n)
    glBindVertexArray(0)


def make_vbo(data):
     
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo


def update_vbo(data, vbo):
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferSubData(GL_ARRAY_BUFFER, 0, data.nbytes, data)
    glBindBuffer(GL_ARRAY_BUFFER, 0)


def draw_vbo(point_data, point_vbo, draw_type, gl_point_size=3):
    n_per_vertice = 3
    n_per_colour = 4
    items_per_point = n_per_vertice + n_per_colour
    stride = point_data.itemsize*items_per_point
    n = point_data.shape[0]

    glBindBuffer(GL_ARRAY_BUFFER, point_vbo)

    # enable vertex followed by color within VBOs
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(n_per_vertice, GL_FLOAT, stride, ctypes.c_void_p(0))

    # calculate color offset (assuming data is tightly packed)
    # color comes after vertex
    glEnableClientState(GL_COLOR_ARRAY)
    glColorPointer(n_per_colour, GL_FLOAT, stride, ctypes.c_void_p(n_per_vertice * point_data.itemsize))

    # draw VBO
    glPointSize(gl_point_size)
    glDrawArrays(draw_type, 0, n)

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
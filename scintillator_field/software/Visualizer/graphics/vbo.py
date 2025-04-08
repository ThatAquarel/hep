from OpenGL.GL import *


def create_vao(
    data,
    v_ptr=3,
    c_ptr=3,
    n_ptr=3,
    return_vbo=False,
    store_normals=False,
):
    """
    Create OpenGL Vertex Array Object (VAO), bind a
    Vertex Buffer Object (VBO) and copy data into it

    :param data: Array of float32 to copy into VBO
    :param v_ptr: Vertex pointer size of 4 bytes (float32)
    :param c_ptr: Color pointer size of 4 bytes (float32)
    :param n_ptr: Normal pointer size of 4 bytes (float32)
    :param return_vbo: Return internal VBO object pointer
    :param store_normals: Use normal pointer
    :return: VAO or (VAO, VBO)
    """

    # total number of float32s for every vertex
    len_ptr = v_ptr + c_ptr + (n_ptr if store_normals else 0)
    # length in bytes for data of every vertex
    stride = len_ptr * data.itemsize

    # vertex array object
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    # vertex buffer object binded to VAO
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    # copy data
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)

    # set vertex position pointer position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    # enable at pointer of index 0
    # see joule/graphics/shaders/vertex.glsl
    # matches with:
    #   layout(location = 0) in vec3 position;
    glEnableVertexAttribArray(0)

    # color pointer offset in bytes
    # color right after vertex position
    c_offset = v_ptr * data.itemsize
    # set color pointer position
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(c_offset))
    # enable at pointer of index 1
    # see joule/graphics/shaders/vertex.glsl
    # matches with:
    #   layout(location = 1) in vec3 color;
    glEnableVertexAttribArray(1)

    if store_normals:
        # optionally compute normals offset
        # normal pointer offset in bytes
        # normal right after vertex positiion and color
        n_offset = (v_ptr + c_ptr) * data.itemsize
        # set normal pointer position
        glVertexAttribPointer(
            2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(n_offset)
        )
        # enable at pointer of index 2
        # see joule/graphics/shaders/vertex.glsl
        # matches with:
        #   layout(location = 2) in vec3 normal;
        glEnableVertexAttribArray(2)

    # unbind VAO and VBO
    # to not have issues later on...
    # (found this one out the hard way!)
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    # optionally returns VBO
    if return_vbo:
        return vao, vbo

    return vao


def update_vbo(
    vbo,
    data,
):
    """
    Update OpenGL Vertex Buffer Object (VBO) with new data

    :param data: Array of float32 to copy into VBO
    """

    # bind VBO
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    # change VBO data
    glBufferSubData(GL_ARRAY_BUFFER, 0, data.nbytes, data)

    # unbind VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)


def draw_vao(
    vao,
    draw_type,
    n,
):
    """
    Draw OpenGL Vertex Array Object (VAO)

    :param vao: OpenGL VAO
    :param draw_type: OpenGL draw mode (ie: GL_TRIANGLES, GL_LINES, etc.)
    :param n: Number of objects to draw
    """

    # bind VAO
    glBindVertexArray(vao)

    # draw VBO of VAO
    glDrawArrays(draw_type, 0, n)

    # unbind VAO
    glBindVertexArray(0)

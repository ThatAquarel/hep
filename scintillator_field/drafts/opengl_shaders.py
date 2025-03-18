import os

import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GL import glViewport, glReadPixels, GL_DEPTH_COMPONENT, GL_FLOAT


import glfw
import numpy as np


FRAGMENT = """
#version 330 core

in vec3 vertex_color;

out vec4 fragColor;

void main() {
    fragColor = vec4(vertex_color, 1.0);
}
"""


VERTEX = """
#version 330 core

// vertex buffer object data
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;

// transformation matrix constants
uniform mat4 world_transform;
uniform mat4 cam_projection;
uniform mat4 cam_transform;

// parameters passed to fragment shader
out vec3 vertex_color;

void main() {
    // modelview matrix taking into account
    // the camera's panning and rotations
    mat4 t = world_transform * cam_transform;
    // 3D points are transformed, then projected onto a 2D screen
    gl_Position = vec4(position, 1.0) * t * cam_projection;

    // pass these parameters down to the fragment shader
    // the color of each point
    vertex_color = color;
}
"""


def create_vao(
    data,
    v_ptr=3,
    c_ptr=3,
    return_vbo=False,
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
    len_ptr = v_ptr + c_ptr
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


class ShaderRenderer:
    def __init__(self, **kwargs):
        """
        Shader Renderer: Accelerates via GPU lighting computations
        and rendering of frames, and sets up the drawing context
        necessary for OpenGL to function
        """

        super().__init__(**kwargs)

        # self._transform is this 4x4 matrix
        # that transforms between the physics coordinate
        # system and the OpenGL coordinate system
        # physics:
        #   +X towards right
        #   +Y into screen
        #   +Z towards up
        # OpenGL:
        #   +X towards right
        #   +Y towards up
        #   +Z into screen
        #
        # this matrix swaps Y->Z and Z->Y
        # so that the physics engine's computations can
        # be displayed in their correct orientation in
        # OpenGL
        #
        # 1.0, 0.0, 0.0, 0.0
        # 0.0, 0.0, 1.0, 0.0
        # 0.0, 1.0, 0.0, 0.0
        # 0.0, 0.0, 0.0, 1.0

        self._transform = glm.mat4x4(
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
        )

        # camera view vector in OpenGL coordinate system
        # camera is looking 32 units into Z (screen)
        self._view_vec = glm.vec4(0, 0, 32, 1)

    def get_right_handed(self):
        """
        Return conversion transformation matrix from the
        right-handed physics coordinate system

        :return: Matrix of shape (4, 4)
        """

        return self._transform

    def _load_shader_source(self, source, type):
        """
        Load a shader from source that is contained within the
        joule.graphics.shaders namespace

        :param file: File name of shader
        :param type: Type of shader: GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
        :return: OpenGL compiled shader
        """

        # return compiled
        return compileShader(source, type)

    def _load_shader(self):
        """
        Load main renderer shaders from source, and compile as
        program for rendering pipeline

        :return: OpenGL compiled shader program
        """

        # load vertex shader (for transforming vertices)
        v_shader = self._load_shader_source(VERTEX, GL_VERTEX_SHADER)

        # load fragment shader (for computing lighting)
        f_shader = self._load_shader_source(FRAGMENT, GL_FRAGMENT_SHADER)

        # return combined OpenGL shader pipeline
        return compileProgram(v_shader, f_shader)

    def _uniform_float(self, name, value):
        """
        Set float shader uniform value

        :param name: Name of uniform
        :param value: New value of uniform
        """

        location = glGetUniformLocation(self._shader, name)
        glUniform1f(location, value)

    def _uniform_vec3(self, name, glm_vec3):
        """
        Set vec3 shader uniform value

        :param name: Name of uniform
        :param value: New vec3 of uniform
        """

        location = glGetUniformLocation(self._shader, name)
        glUniform3fv(location, 1, glm.value_ptr(glm_vec3))

    def _uniform_mat4(self, name, glm_mat4):
        """
        Set matrix 4x4 shader uniform value

        :param name: Name of uniform
        :param value: New matrix 4x4 of uniform
        """

        location = glGetUniformLocation(self._shader, name)
        glUniformMatrix4fv(location, 1, GL_TRUE, glm.value_ptr(glm_mat4))

    def render_setup(self):
        """
        Setup rendering pipeline on program initialize
        """

        # load shader pipeline
        self._shader = self._load_shader()

        # enable depth to compute visual occlusion of objects
        glEnable(GL_DEPTH_TEST)

        # enable antialiasing (smooth lines)
        glEnable(GL_MULTISAMPLE)

        # enable opacity (transparency)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

    def frame_setup(self, background_color):
        """
        Setup rendering pipeline on each frame

        :param background_color: Screen background color as vector of shape (3,)
        """

        # clear color and depth cache from previous frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # set background color
        glClearColor(*background_color, 1.0)

        # use shader
        glUseProgram(self._shader)

    def set_matrix_uniforms(
        self,
        cam_projection,
        cam_transform,
    ):
        """
        Supply camera and world matrix transforms to shader to
        project 3D coordinates onto screen using GPU acceleration

        :param cam_projection: Orthographic projection matrix of shape (4, 4)
        :param cam_transform: Camera view transformation matrix of shape (4, 4)
        """

        # pass values into shader
        # see joule/graphics/shaders/vertex.glsl
        # the values are plugged into the shader as constants
        #   uniform mat4 world_transform;
        #   uniform mat4 cam_projection;
        #   uniform mat4 cam_transform;
        #
        # all subsequent dot products are done with these values,
        # which accelerates 3D point transformation with GPU

        self._uniform_mat4("world_transform", self.get_right_handed())
        self._uniform_mat4("cam_projection", cam_projection)
        self._uniform_mat4("cam_transform", cam_transform)


class CameraOrbitControls:
    def __init__(
        self,
        zoom_sensitivity=0.1,
        pan_sensitvity=0.001,
        orbit_sensitivity=0.0025,
        initial_zoom=5,
        initial_view_angle=(np.pi / 6, np.pi / 4),
        clipping=[-32, 32],
        **kwargs,
    ):
        """
        Camera Orbit Controls: Manages mouse camera movement
        to translate, rotate, and scale current view with
        orthographic projection

        :param zoom_sensitivity: Mouse scroll to view scale ratio
        :param pan_sensitvity:  Mouse move to view translate ratio
        :param orbit_sensitivity: Mouse move to view rotate ratio
        :param initial_zoom: Initial view scale
        :param initial_view_angle: Initial X and Y view angle in radians
        :param clipping: Clipping planes for orthographic projection
        """
        super().__init__(**kwargs)

        # constants
        self._zoom_sensitivity = zoom_sensitivity
        self._pan_sensitivity = pan_sensitvity
        self._orbit_sensitivity = orbit_sensitivity

        self._zoom_level = initial_zoom
        self._clipping = clipping

        # vector states
        self._view_angle = np.array(initial_view_angle)
        self._view_pan = np.zeros(2)
        self._view_box = np.zeros(2)
        self._prev_mouse_pos = np.zeros(2)

        # store internal state
        # when dragging           -> rotation
        # when dragging + panning -> translation
        self._dragging, self._panning = False, False

    def camera_mouse_button_callback(self, window, button, action, mods):
        """
        Mouse button event callback handler

        :param window: glfw window
        :param button: glfw button
        :param action: glfw action
        :param mods: glfw modifiers
        """

        # filter for right clicks which are
        # for camera movements
        if button != glfw.MOUSE_BUTTON_RIGHT:
            return

        # dragging when: right mouse button held
        self._dragging = action == glfw.PRESS

        # panning when: ctrl + right mouse button held
        self._panning = glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS

    def camera_cursor_pos_callback(self, window, x_pos, y_pos):
        """
        Mouse position event callback handler

        :param window: glfw window
        :param x_pos: mouse x-coordinate with respect to top left corner
        :param y_pos: mouse y-coordinate with respect to top left corner
        """

        # vectorize mouse position
        mouse_pos = [x_pos, y_pos]

        if self._dragging:

            # change in mouse position over one frame
            ds = mouse_pos - self._prev_mouse_pos

            if self._panning:
                # adjust pan according to zoom
                # so that translation is always constant,
                # independent of zoom
                zoomed_pan = self._pan_sensitivity * self._zoom_level

                # updates translation vector
                # [1, -1] flips the y position as OpenGL's origin
                # is at the bottom left corner instead of top left
                self._view_pan += ds * [1, -1] * zoomed_pan
            else:

                # updates rotation vector
                # [::-1] reverses the order, effectively mapping the
                # x screen position onto the OpenGL's x rotation and
                # y screen position onto the OpenGL's y rotation
                self._view_angle += ds[::-1] * self._orbit_sensitivity

        # save previous to calculate the next delta
        self._prev_mouse_pos[:] = mouse_pos

    def camera_scroll_callback(self, window, x_offset, y_offset):
        """
        Mouse scroll event callback handler

        :param window: glfw window
        :param x_offset: mouse horizontal scrollwheel change
        :param y_offset: mouse vertical scrollwheel change
        """

        # scroll up: zoom in
        if y_offset > 0:
            self._zoom_level /= 1 + self._zoom_sensitivity

        # scroll down: zoom out
        elif y_offset < 0:
            self._zoom_level *= 1 + self._zoom_sensitivity

    def camera_resize_callback(self, window, width, height):
        """
        Window resize event callback handler

        :param window: glfw window
        :param width: new window width
        :param height: new window height
        """

        # update rendering shape
        glViewport(0, 0, width, height)

        # compute aspect ratio, so that the render
        # is not stretched if the window is stretched
        # bugfix: on X11 Ubuntu 20.04, the height starts
        # at zero when the window is first rendered, so we
        # prevent a zero division error
        aspect_ratio = width / height if height > 0 else 1.0

        # update the camera view coordinates with screen ratio
        self._view_box[:] = [-aspect_ratio, aspect_ratio]

    def get_camera_projection(self):
        """
        Computes a orthographic projection matrix
        with the internal view parameters

        :return: Orthographic projection matrix of shape (4, 4)
        """

        p = glm.ortho(
            *self._view_box * self._zoom_level,
            -self._zoom_level,
            self._zoom_level,
            *self._clipping,
        )

        return p

    def get_camera_transform(self):
        """
        Computes the view transformation matrix
        with the internal view parameters

        :return: Camera view transformation matrix of shape (4, 4)
        """

        # compose matrix transformations
        # first translate for panning
        t = glm.translate(glm.vec3(*self._view_pan, 0.0))

        # then rotate on X and Y axes
        t = glm.rotate(t, self._view_angle[0], (1.0, 0.0, 0.0))
        t = glm.rotate(t, self._view_angle[1], (0.0, 1.0, 0.0))

        return t

    def get_click_point(self, window, world_transform):
        """
        Unprojects a 2D click on the window into 3D coordinates
        with respect to the internalal view parameters

        :param window: glfw window of click
        :param world_transform: Other transformation not included in view

        :return: Coordinates of click as vector of shape (3,)
        """

        # get current mouse click position on window
        xpos, ypos = glfw.get_cursor_pos(window)
        win_x, win_y = glfw.get_window_size(window)

        # transform window coordinates into OpenGL coordinates
        # by flipping y-axis (I found this out the hard way.)
        ypos = win_y - ypos

        # read depth component of current frame
        depth = glReadPixels(xpos, ypos, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)

        # vectorize the click
        click = glm.vec3(xpos, ypos, depth)

        # determine compounded projection from point to frame
        # can determine the click coordinates
        pos = self.get_camera_transform()
        modelview = pos * world_transform
        proj = self.get_camera_projection()

        # vectorize the viewport
        viewport = glm.vec4(0, 0, win_x, win_y)

        # unproject: send out a ray from where the window was clicked
        # that goes until it meets the depth from the depth buffer,
        # which is the ray's endpoint (the 3D coordinate of click)
        return glm.unProject(click, modelview, proj, viewport)


class App(CameraOrbitControls, ShaderRenderer):
    def __init__(
        self,
        window_size,
        name,
        *orbit_control_args,
    ):
        """
        Joule App: Main class for application

        Extends: CameraOrbitControls, ShaderRenderer

        :param window_size: Initial window size (width, height)
        :param name: Initial window name
        """

        # init camera orbit controls and shader renderer
        super().__init__(*orbit_control_args)

        # initialize window
        self.window = self.window_init(window_size, name)

        # fall into rendering loop
        self.rendering_loop()

    def window_init(self, window_size, name):
        # throw exception if glfw failed to init
        if not glfw.init():
            raise Exception("GLFW could not be initialized.")

        if os.name == "posix":
            # macos config
            glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
            glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
            glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        elif os.name == "nt":
            # windows flags
            ...

        # enable multisampling (antialiasing) on glfw window
        glfw.window_hint(glfw.SAMPLES, 4)

        # create window and context
        window = glfw.create_window(*window_size, name, None, None)
        if not window:
            glfw.terminate()
            raise Exception("GLFW window could not be created.")
        glfw.make_context_current(window)

        # wrapper callback functions to dispatch events to ui and camera
        glfw.set_cursor_pos_callback(window, self.cursor_pos_callback)
        glfw.set_mouse_button_callback(window, self.mouse_button_callback)
        glfw.set_scroll_callback(window, self.scroll_callback)
        glfw.set_framebuffer_size_callback(window, self.resize_callback)

        glfw.set_key_callback(window, self.key_callback)
        glfw.set_char_callback(window, self.char_callback)

        # initially call window resize to rescale frame
        self.camera_resize_callback(window, *window_size)

        return window

    def key_callback(self, *args):
        pass
        # forward ui keyboard callbacks
        # if self.ui.want_keyboard:
        #     self.ui.impl.keyboard_callback(*args)

    def char_callback(self, *args):
        pass
        # forward ui keyboard callbacks
        # if self.ui.want_keyboard:
        #     self.ui.impl.char_callback(*args)

    def mouse_button_callback(self, window, button, action, mods):
        # forward ui mouse callbacks
        # if self.ui.want_mouse:
        #     return

        # forward camera mouse callbacks
        self.camera_mouse_button_callback(window, button, action, mods)

        # # add ball: left click
        # if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        #     self.on_add(window)

    def cursor_pos_callback(self, window, xpos, ypos):
        # forward camera mouse callbacks
        self.camera_cursor_pos_callback(window, xpos, ypos)

    def scroll_callback(self, window, xoffset, yoffset):

        # forward camera mouse callbacks
        self.camera_scroll_callback(window, xoffset, yoffset)

    def resize_callback(self, window, width, height):
        # forward camera window callback
        self.camera_resize_callback(window, width, height)

    def window_should_close(self):
        return glfw.window_should_close(self.window)

    def rendering_loop(self):
        """
        Main rendering loop for application
        """

        self.render_setup()

        # Define the 8 vertices of the unit cube
        vertices = np.array(
            [
                [0, 0, 0],
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0],
                [0, 0, 1],
                [1, 0, 1],
                [1, 1, 1],
                [0, 1, 1],
            ]
        )

        # Define the 12 triangles (two per face)
        triangles = np.array(
            [
                [0, 1, 2],
                [0, 2, 3],  # Bottom face
                [4, 5, 6],
                [4, 6, 7],  # Top face
                [0, 1, 5],
                [0, 5, 4],  # Front face
                [1, 2, 6],
                [1, 6, 5],  # Right face
                [2, 3, 7],
                [2, 7, 6],  # Back face
                [3, 0, 4],
                [3, 4, 7],  # Left face
            ]
        )

        cube_vertices = vertices[triangles].reshape((-1, 3))
        color = np.random.rand(len(cube_vertices), 3)
        cube = np.hstack((cube_vertices, color)).astype(np.float32)

        vao = create_vao(cube)

        # main rendering loop until user quits
        while not self.window_should_close():
            # setup frame rendering with OpenGL calls
            self.frame_setup((0.2, 0.2, 0.2))

            # shader: update camera matrices
            self.set_matrix_uniforms(
                self.get_camera_projection(),
                self.get_camera_transform(),
            )

            draw_vao(vao, GL_TRIANGLES, len(cube))

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()


if __name__ == "__main__":

    # run the app
    App((1280, 720), "Joule")

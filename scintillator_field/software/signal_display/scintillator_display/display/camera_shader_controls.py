import numpy as np

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import os

class CameraShaderControls:
    def __init__(self,
                 angle_sensitivity=0.001,
                 zoom=251,
                 clear_colour=(0.5,)*3):
        
        
        self.set_initial_camera_values(angle_sensitivity, zoom, clear_colour)

    def set_initial_camera_values(self, angle_sensitivity, zoom, clear_colour):

        self.pan_sensitivity   = 0.001
        self.angle_sensitivity = angle_sensitivity

        self.pan_x, self.pan_y, self.pan_z = 0, 0, 0
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0
        self.zoom = zoom

        self.mouse_dragging = False
        self.panning, self.angling = False, False
        self.last_x, self.last_y = 0,0

        self.width, self.height = 1924, 1080
        self.aspect_ratio = self.width/self.height
        self.render_distance = 512

        self.view_vec = (0, 0, 32, 1)

        self.clear_colour = clear_colour

        self.light_color = (1, 1, 1)

        self.ambient_strength = 0.2
        self.diffuse_strength = 0.2
        self.diffuse_base = 0.3
        self.specular_strength = 0.1
        self.specular_reflection = 16.0


    def transformation_matrix(self, t=(0,0,0), r=(0,0,0)):
        tx, ty, tz = t
        drx, dry, drz = r # degrees
        rrx, rry, rrz = np.radians(drx), np.radians(dry), np.radians(drz),

        translation = np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]])
        
        rot_x = np.array([
            [1,            0,           0, 0],
            [0,  np.cos(rrx), np.sin(rrx), 0],
            [0, -np.sin(rrx), np.cos(rrx), 0],
            [0,            0,           0, 1]])

        rot_y = np.array([
            [np.cos(rry), 0, -np.sin(rry), 0],
            [          0, 1,            0, 0],
            [np.sin(rry), 0,  np.cos(rry), 0],
            [          0, 0,            0, 1]])

        rot_z = np.array([
            [np.cos(rrz), -np.sin(rrz), 0, 0],
            [np.sin(rrz),  np.cos(rrz), 0, 0],
            [          0,            0, 1, 0],
            [          0,            0, 0, 1],])

        
        transformation_matrix = translation @ rot_x @ rot_y @ rot_z

        return transformation_matrix

    def get_orthographic_projection(self):
        
        (l, r, b, t, n, f) = (-self.aspect_ratio * self.zoom,
                               self.aspect_ratio * self.zoom,
                              -self.zoom,
                               self.zoom,
                              -self.render_distance,
                               self.render_distance)
        orthographic_projection = np.array([
            [2/(r-l), 0, 0, 0],
            [0, 2/(t-b), 0, 0],
            [0, 0, 2/(f-n), 0],
            [-(r+l)/(r-l), -(t+b)/(t-b), -(f+n)/(f-n), 1],
        ])

        return orthographic_projection

    def get_camera_tranform(self):
        camera_transform = self.transformation_matrix(
            t=(self.pan_x, self.pan_y, self.pan_z),
            r=(self.angle_x, self.angle_y, self.angle_z)
        )
        return camera_transform

    def get_world_transform(self):
        right_handed = np.array([
            [1,0,0,0],
            [0,0,1,0],
            [0,1,0,0],
            [0,0,0,1],
        ])
        return right_handed

    def get_vertex_shader_text(self):
        this_file_path = os.path.abspath(__file__)
        lst_f_path = this_file_path.split(os.sep)

        vertex_path = lst_f_path.copy()
        vertex_path[-1] = "vertex_shader.glsl"
        vertex_path   = os.sep.join(vertex_path)
        
        with open(vertex_path, "r") as f:
            vertex_shader_text = f.read()
        
        return vertex_shader_text

    def get_fragment_shader_text(self):
        
        this_file_path = os.path.abspath(__file__)
        lst_f_path = this_file_path.split(os.sep)

        fragment_path = lst_f_path.copy()
        fragment_path[-1] = "fragment_shader.glsl"
        fragment_path   = os.sep.join(fragment_path)
        
        with open(fragment_path, "r") as f:
            fragment_shader_text = f.read()
        
        return fragment_shader_text

    def make_shader_program(self):
        vertex_text = self.get_vertex_shader_text()
        vertex_shader = compileShader(vertex_text, GL_VERTEX_SHADER)

        fragment_text = self.get_fragment_shader_text()
        fragment_shader = compileShader(fragment_text, GL_FRAGMENT_SHADER)
        
        self.shader_program = compileProgram(vertex_shader, fragment_shader, validate=False)

    def set_uniform_float(self, uniform_name, num):
        location = glGetUniformLocation(self.shader_program, uniform_name)
        glUniform1f(location, num)

    def set_uniform_vec3(self, uniform_name, vec3):
        location = glGetUniformLocation(self.shader_program, uniform_name)
        glUniform3fv(location, 1, vec3)

    def set_uniform_mat4(self, uniform_name, mat4):
        location = glGetUniformLocation(self.shader_program, uniform_name)
        glUniformMatrix4fv(location, 1, GL_TRUE, mat4)

    def setup_opengl(self):

        self.make_shader_program()

        # enable depth to compute visual occlusion of objects
        glEnable(GL_DEPTH_TEST)

        # enable antialiasing (smooth lines)
        glEnable(GL_MULTISAMPLE)
        # glEnable(GL_POINT_SMOOTH)

        # enable opacity (transparency)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

    def begin_render_gl_actions(self):
        # set background color
        glClearColor(*self.clear_colour, 1.0)

        # Dual-viewports: Clear bufferbit after clear color
        # clear color and depth cache from previous frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # use shader
        glUseProgram(self.shader_program)

        self.set_uniforms()

    def set_uniforms(self):
        camera_transform = self.get_camera_tranform()

        self.set_uniform_mat4("world_transform" , self.get_world_transform())
        self.set_uniform_mat4("cam_transform"   , camera_transform)
        self.set_uniform_mat4("ortho_projection", self.get_orthographic_projection())

        view_pos = np.linalg.inv(camera_transform) * self.view_vec

        self.set_uniform_vec3("view_pos" , view_pos)
        self.set_uniform_vec3("light_pos", view_pos)

        self.set_uniform_vec3("light_color", self.light_color)

        self.set_uniform_float("ambient_strength"   , self.ambient_strength)
        self.set_uniform_float("diffuse_strength"   , self.diffuse_strength)
        self.set_uniform_float("diffuse_base"       , self.diffuse_base)
        self.set_uniform_float("specular_strength"  , self.specular_strength)
        self.set_uniform_float("specular_reflection", self.specular_reflection)



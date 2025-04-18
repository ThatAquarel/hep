from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileShader, compileProgram

import os
import sys

import numpy as np

class Shaders:
    def __init__(self):
        pass


    def set_mat4_uniform(self, shader_program, uniform_name, mat4):
        uniform_location = glGetUniformLocation(shader_program, uniform_name)
        glUniformMatrix4fv(uniform_location, 1, GL_TRUE, mat4)



    def make_uniforms(self, shader_program, window):

        
        (l, r, b, t, n, f) = (-window.aspect_ratio * window.zoom,
                            window.aspect_ratio * window.zoom,
                            -window.zoom,
                            window.zoom,
                            -window.render_distance,
                            window.render_distance)
        orthographic_projection = np.array([
            [2/(r-l), 0, 0, 0],
            [0, 2/(t-b), 0, 0],
            [0, 0, 2/(f-n), 0],
            [-(r+l)/(r-l), -(t+b)/(t-b), -(f+n)/(f-n), 1],
        ])



        camera_translation = self.translate(window.pan_x, window.pan_y, window.pan_z)
        camera_rotation = self.rotate(window.angle_x, window.angle_y, window.angle_z)

        camera_transformation = camera_translation @ camera_rotation


        inv_cam_transform = np.linalg.inv(camera_transformation)


        #world_transform = np.eye(4)

        world_transform = np.array([
            [1,0,0,0],
            [0,0,1,0],
            [0,1,0,0],
            [0,0,0,1],
        ])


        self.set_mat4_uniform(shader_program, "orthographic_projection", orthographic_projection)
        self.set_mat4_uniform(shader_program, "camera_transformation", camera_transformation)
        self.set_mat4_uniform(shader_program, "inv_cam_transform", inv_cam_transform)
        self.set_mat4_uniform(shader_program, "world_transform", world_transform)

    
    def translate(self, x, y, z):
        translation = np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]])
        
        return translation
    

    def rotate(self, rx, ry, rz):

        rrx, rry, rrz = np.radians(rx), np.radians(ry), np.radians(rz),
        
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
        
        return rot_x @ rot_y @ rot_z

    def make_shaders(self):


        this_file_path = os.path.abspath(__file__)
        lst_f_path = this_file_path.split(os.sep)

        vertex_path = lst_f_path.copy()
        fragment_path = lst_f_path.copy()

        vertex_path[-1] = "vertex_shader.glsl"
        fragment_path[-1] = "fragment_shader.glsl"

        vertex_path   = os.sep.join(vertex_path)
        fragment_path = os.sep.join(fragment_path)

        with open(vertex_path, "r") as f:
            vertex_shader_text = f.read()
        vertex_shader = compileShader(vertex_shader_text, GL_VERTEX_SHADER)

        with open(fragment_path, "r") as f:
            fragment_shader_text = f.read()
        fragment_shader = compileShader(fragment_shader_text, GL_FRAGMENT_SHADER)
        
        shader_program = compileProgram(vertex_shader, fragment_shader, validate=False)


        return shader_program
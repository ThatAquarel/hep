#version 330 core

layout (location = 0) in vec3 point_pos;
layout (location = 1) in vec4 point_col;

out vec4 vertex_colour;

// uniform mat4 inv_cam_transform;
// uniform mat4 orthographic_projection;
// uniform mat4 camera_transformation;
// uniform mat4 model_transform;

uniform mat4 orthographic_projection;
uniform mat4 camera_transformation;
uniform mat4 inv_cam_transform;
uniform mat4 world_transform;

void main() {
    gl_Position = orthographic_projection * camera_transformation * world_transform * vec4(point_pos, 1.0);
    //gl_Position = orthographic_projection * camera_transformation * model_transform * vec4(point_pos, 1.0);
    vertex_colour = point_col;
}
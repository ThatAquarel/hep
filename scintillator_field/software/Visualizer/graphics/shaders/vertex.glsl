#version 330 core

// vertex buffer object data
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;
layout(location = 2) in vec3 normal;

// transformation matrix constants
uniform mat4 world_transform;
uniform mat4 cam_projection;
uniform mat4 cam_transform;

// parameters passed to fragment shader
out vec3 vertex_color;
out vec3 vertex_normal;
out vec3 vertex_frag_pos;

void main() {
    // modelview matrix taking into account
    // the camera's panning and rotations
    mat4 t = world_transform * cam_transform;
    // 3D points are transformed, then projected onto a 2D screen
    gl_Position = vec4(position, 1.0) * t * cam_projection;

    // pass these parameters down to the fragment shader
    // the color of each point
    vertex_color = color;
    
    // transform the normal and position with respect to the
    // rendering coordinate system
    vertex_normal = vec3(vec4(normal, 1.0) * world_transform);
    vertex_frag_pos = vec3(vec4(position, 1.0) * world_transform);
}

#version 330 core

in vec4 vertex_colour;

out vec4 fragment_colour;

// uniform vec3 ambient_light;
// 
// uniform float ambient_strength;

void main() {
    // vec3 ambient = ambient_strength * ambient_light;
// 
// 
    // vec4 final_colour = vec4(ambient, 1.0) * vertex_colour;
// 
    // fragment_colour = final_colour;

    fragment_colour = vertex_colour;
}
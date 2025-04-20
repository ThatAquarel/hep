#version 330 core

in vec4 vertex_colour;

out vec4 fragment_colour;


void main() {
    fragment_colour = vertex_colour;
}
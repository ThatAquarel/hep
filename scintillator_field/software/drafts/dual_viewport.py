import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# Global variables for view control
angle_x, angle_y = 0.0, 0.0
pan_x, pan_y = 0.0, 0.0
last_x, last_y = 0.0, 0.0
dragging = False
panning = False

width, height = 800, 800


def initialize_glfw():
    global width, height

    if not glfw.init():
        raise Exception("GLFW could not be initialized.")

    window = glfw.create_window(
        width, height, "Orthographic Axes with Mouse Drag and Pan", None, None
    )
    if not window:
        glfw.terminate()
        raise Exception("GLFW window could not be created.")

    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    return window


def setup_orthographic_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -0.5, 1.5, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def draw_axes():
    glBegin(GL_LINES)

    # X axis (red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)

    # Y axis (green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)

    # Z axis (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -1.0)
    glVertex3f(0.0, 0.0, 1.0)

    glEnd()


def apply_view_transformations():
    global angle_x, angle_y, pan_x, pan_y
    glTranslatef(pan_x, pan_y, 0.0)
    glRotatef(angle_x, 1.0, 0.0, 0.0)
    glRotatef(angle_y, 0.0, 1.0, 0.0)


def mouse_callback(window, xpos, ypos):
    global last_x, last_y, angle_x, angle_y, pan_x, pan_y, dragging, panning
    if dragging:
        dx = xpos - last_x
        dy = ypos - last_y
        if panning:
            # Pan the view
            pan_x += dx * 0.001
            pan_y -= dy * 0.001
        else:
            # Rotate the view
            angle_x += dy * 0.1
            angle_y += dx * 0.1
    last_x, last_y = xpos, ypos


def mouse_button_callback(window, button, action, mods):
    global dragging, panning
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            dragging = True
            panning = False
        elif action == glfw.RELEASE:
            dragging = False
    elif button == glfw.MOUSE_BUTTON_MIDDLE:
        if action == glfw.PRESS:
            dragging = True
            panning = True
        elif action == glfw.RELEASE:
            dragging = False
            panning = False


def main():
    global last_x, last_y
    window = initialize_glfw()

    # Initial cursor position
    last_x, last_y = glfw.get_cursor_pos(window)

    setup_orthographic_projection()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(245 / 255, 247 / 255, 248 / 255, 1.0)

        glViewport(0, 0, width // 2, height)

        glLoadIdentity()
        apply_view_transformations()

        draw_axes()

        glViewport(width // 2, 0, width, height)

        glLoadIdentity()
        apply_view_transformations()

        draw_axes()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()

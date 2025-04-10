import glm
import glfw
import numpy as np


from OpenGL.GL import glViewport, glReadPixels, GL_DEPTH_COMPONENT, GL_FLOAT


class CameraOrbitControls:
    def __init__(
        self,
        zoom_sensitivity=0.1,
        pan_sensitvity=0.001,
        orbit_sensitivity=0.0025,
        initial_zoom=5,
        initial_view_angle=(np.pi / 6, np.pi / 4),
        clipping=[-512, 512],
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
        # depth = self._zoom_level
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

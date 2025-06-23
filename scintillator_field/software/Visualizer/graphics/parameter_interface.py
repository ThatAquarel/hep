import imgui
from imgui.integrations.glfw import GlfwRenderer

import numpy as np

import graphics.orbit_controls

import test


def ui_spacing():
    """
    Creates a blank space in the user interface
    """

    for _ in range(5):
        imgui.spacing()


def ui_section(section_name, top_margin=True):
    """
    Decorator constructor to wrap a user interface
    section with a title: reduce the repetition
    of creating a separation for every section
    """

    # constructed decorator
    def decorator(func):
        # wrap the method, building the title
        # of the section first, before drawing
        # the rest of the section

        def wrapper(*args, **kwargs):
            if top_margin:
                ui_spacing()

            # display section title
            imgui.text(section_name)
            imgui.separator()

            # draw the rest of the section
            func(*args, **kwargs)

        return wrapper

    return decorator


class ParameterInterface:
    def __init__(
        self,
        window,
    ):
        """
        Parameter Interface: Manages the state of the parameters
        controlled by the user, and draws the interface

        :param window: glfw window
        :param on_evaluate: Callback for a new user function's evaluation call
        :param on_change_ball_color: Callback to change ball color
        :param on_change_surface_color: Callback to change surface color
        """

        # create DearImGui instance for ui drawing
        imgui.create_context()

        # create bindings to Glfw rendering backend
        # the application manages its own callbacks
        self._imgui_impl = GlfwRenderer(window, attach_callbacks=False)



        # camera data
        self.camera = graphics.orbit_controls.CameraOrbitControls()

        self.light_color = [1.0, 1.0, 1.0]
        self.background_color = [0.86, 0.87, 0.87]

        self.ambient_strength = 0.2
        self.diffuse_strength = 0.2
        self.diffuse_base = 0.3
        self.specular_strength = 0.1
        self.specular_reflection = 16.0

        #elements
        self.dataset_active = []
        for i in range(len(test.data)):
            self.dataset_active.append(False)

        self.show_axes = True
        self.latest = True

        self.pt_selected_send = False




    @property
    def want_keyboard(self):
        return imgui.get_io().want_capture_keyboard

    @property
    def want_mouse(self):
        return imgui.get_io().want_capture_mouse

    @property
    def impl(self):
        return self._imgui_impl
    
    @ui_section("Status", top_margin=False)
    def status(self):
        
        _, self.show_axes = imgui.checkbox("show xy axes", self.show_axes)
        imgui.text("x-axis: red, y-axis: green, z-axis:blue")


        _, self.latest = imgui.checkbox("Only show last data", self.latest)

        #To update the list of dataset which is active
        if self.latest:
            self.dataset_active = []
            for i in range(len(test.data)):
                self.dataset_active.append(False)
            self.dataset_active[-1] = True


    @ui_section("Point data")
    def point_data(self,pt_selected):
        
        if pt_selected == None:
            imgui.text(f"No data point selected")

        else:
            for i in range(len(self.dataset_active)):
                #To prevent the selected point of previous data set which is no longer showing
                if pt_selected in test.data[i] and not self.dataset_active[i]:
                    self.pt_selected_send = None   #This thing tells app.py to change back the pt_selected 
                    imgui.text(f"No data point selected")
                    return 
                
                #To find the data of the point selected
                elif self.dataset_active[i]:
                    for pt in test.data[i]:
                        if pt_selected == pt:
                            set_number = i + 1
                            point = test.data[i].index(pt_selected) + 1

            imgui.text(f"Dataset #{set_number}")
            imgui.text(f"Point #{point}")
            imgui.text(f"Coordinates: ({pt_selected[0]},{pt_selected[1]})")
            imgui.text(f"Coordinates in Binary(+128): ({bin(pt_selected[0]+128)},{bin(pt_selected[1]+128)})")
            

        


    @ui_section("Tests")
    def tests(self):

        for i in range(len(test.data)):
            _, self.dataset_active[i] = imgui.checkbox(f"Datatest {i + 1}", self.dataset_active[i])
        

        

    def on_render_ui(self,window,pt_selected):
        """
        Renders full user interface on frame
        """


        imgui.new_frame()
        imgui.begin("Code 'borrowed' from Joule")

        self.status()
        self.point_data(pt_selected)
        self.tests()




        imgui.end()
        imgui.render()

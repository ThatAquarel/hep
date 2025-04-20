import scintillator_display.compat.glfw as glfw
import scintillator_display.compat.imgui as imgui

from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

from .load_res import load_texture, load_font

import time


class Controls:
    def __init__(self, impl_a, impl_b):

        self.activate_data_connection(impl_a, impl_b)

        self.width, self.height = 0, 0

        self.show_only_last_data_a = True
        self.show_only_last_data_b = True
        self.open_state = False

        # ffmpeg -i sc_bw.png -vf "scale=-1:48" hep_48.png
        self.hep = load_texture("hep_48.png")
        # ffmpeg -i sc_bw.png -vf "scale=-1:64" sc_64.png
        self.sc = load_texture("sc_64.png")

        self.font = load_font("Poppins-Regular.ttf", 24)

        self.current = time.time()
        self.dt = 0

    
    def viewport_shenanigans(self, vm, ratio_num):
        vp_controls = vm.add_viewport(None, None)
        vm.set_vp_ratio(vp_controls, ratio_num)
        vm.set_on_render(vp_controls, self.on_render)
        vm.set_window_size_callback(vp_controls, self.window_size_callback)


    def window_size_callback(self, window, width, height):
        self.width, self.height = width, height

    def activate_data_connection(self, impl_a, impl_b):
        self.impl_a, self.impl_b = impl_a, impl_b
        self.data_points    = self.impl_a.data_manager.data
        self.impl_a_checked = self.impl_a.data_manager.impl_a_data_is_checked
        self.impl_b_checked = self.impl_b.data_manager.impl_b_data_is_checked

        self.debug_a = self.impl_a.data_manager.debug
        self.debug_b = self.impl_b.data_manager.debug

        self.show_a_axes = self.impl_a.show_axes
        self.show_b_axes = self.impl_b.show_axes
    
    def space_lines(self, n=1):
        for i in range(n):
            imgui.spacing()

    def on_render(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        imgui.set_next_window_position(0, 0, condition=imgui.ONCE)
        imgui.set_next_window_size(self.width, self.height, condition=imgui.ALWAYS)
        imgui.begin(
            " ",
            flags=imgui.WINDOW_NO_RESIZE
            | imgui.WINDOW_NO_MOVE
            | imgui.WINDOW_NO_COLLAPSE,
        )

        imgui.separator()

        imgui.push_font(self.font)
        imgui.text("The Scintillating Chamber")
        imgui.pop_font()

        imgui.separator()

        imgui.image(*self.hep)
        imgui.same_line()
        imgui.image(*self.sc)

        imgui.separator()

        self.space_lines(2)
        fps = 1/self.dt if self.dt != 0 else 0
        imgui.text(f'{fps:.1f} fps')

        #expanded, _ = imgui.collapsing_header("view window info", True)
        #if expanded:
        #    imgui.text("2")


        self.space_lines(3)
        imgui.text("activate in impl:")
        imgui.text(" a    b")
        imgui.separator()

        _, self.debug_a = imgui.checkbox(" ##A", self.debug_a)
        imgui.same_line()
        _, self.debug_b = imgui.checkbox(
            "debug mode", self.debug_b)
        self.impl_a.data_manager.debug = self.debug_a
        self.impl_b.data_manager.debug = self.debug_b


        imgui.separator()

        _, self.show_a_axes = imgui.checkbox(" ##C", self.show_a_axes)
        self.impl_a.show_axes = self.show_a_axes
        imgui.same_line()
        _, self.show_b_axes = imgui.checkbox(
            "show xyz axes", self.show_b_axes)
        self.impl_b.show_axes = self.show_b_axes

        imgui.separator()

        _, self.show_only_last_data_a = imgui.checkbox(" ##B", self.show_only_last_data_a)
        imgui.same_line()
        _, self.show_only_last_data_b = imgui.checkbox(
            "show only most recent data", self.show_only_last_data_b)
        
        if self.impl_a_checked != []:
            if self.show_only_last_data_a:
                for i in range(len(self.impl_a_checked)):
                    self.impl_a_checked[i] = False
                self.impl_a_checked[-1] = True
        if self.impl_b_checked != []:
            if self.show_only_last_data_b:
                for i in range(len(self.impl_b_checked)):
                    self.impl_b_checked[i] = False
                self.impl_b_checked[-1] = True
        
        imgui.separator()

        if (self.data_points != []
            and self.impl_a_checked != []
            and self.impl_b_checked != []):
            for i, j in enumerate(self.data_points):
                _, self.impl_a_checked[i] = imgui.checkbox(f" ##{i}_IMPL_A", self.impl_a_checked[i])
                imgui.same_line()
                _, self.impl_b_checked[i] = imgui.checkbox(f"{j[-2]}, {j[-1]}##{i}_IMPL_B", self.impl_b_checked[i])

        if any(self.impl_a_checked):
            i = max(i for i, v in enumerate(self.impl_a_checked) if v == True)
            self.last_pt_a_selected = self.data_points[i]
        else:
            self.last_pt_a_selected = None
        self.impl_a.pt_selected = self.last_pt_a_selected

        if any(self.impl_b_checked):
            i = max(i for i, v in enumerate(self.impl_b_checked) if v == True)
            self.last_pt_b_selected = self.data_points[i]
        else:
            self.last_pt_b_selected = None
        self.impl_b.pt_selected = self.last_pt_b_selected


        imgui.end()

        end = time.time()
        self.dt = end-self.current
        self.current = end


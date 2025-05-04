import scintillator_display.compat.glfw as glfw
import scintillator_display.compat.imgui as imgui

from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

from .load_res import load_texture, load_font

import time

import numpy as np


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

        self.mode_a_selected = 1
        self.mode_b_selected = 1
        self.data_a_type_shown = 'newest'
        self.data_b_type_shown = 'newest'
        self.drop_downs = [
            ['##m2', self.mode_a_selected, self.impl_a],
            ['##m3', self.mode_b_selected, self.impl_b],
        ]
        self.xyz_axes = [
            ['##xyz1', not self.show_a_axes, self.impl_a], # "not" needed to begin on show
            ['##xyz2', not self.show_b_axes, self.impl_b], # "not" needed to begin on show
        ]
        self.data_shown = [
            ['##state1', 0, self.data_a_type_shown],
            ['##state2', 0, self.data_b_type_shown],
        ]
        self.checked_data = [self.impl_a_checked, self.impl_b_checked]
        self.point_info = [self.data_points_a, self.data_points_b]



    
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
        self.data_points_a  = self.impl_a.data_manager.data
        self.data_points_b  = self.impl_b.data_manager.data
        self.impl_a_checked = self.impl_a.data_manager.impl_a_data_is_checked
        self.impl_b_checked = self.impl_b.data_manager.impl_b_data_is_checked

        self.mode_a = self.impl_a.data_manager.mode
        self.mode_b = self.impl_b.data_manager.mode

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


        self.space_lines(4)



        self.space_lines(4)


        def set_static_choices(row, column):
            impl_boxes = ["    ", "impl a        ", "impl_b        "]
            modes = ['data', 'debug', 'demo']
            xyz = ['show', 'hide']
            #xyz = ['hide', 'show']
            xy2 = [False, True]
            #xy2 = [True, False]
            data_shown_types = ['newest', 'any', 'none']
            

            if row==0:
                imgui.text(impl_boxes[column])
                pass

            elif row==1:
                if column==0:
                    pass
                    imgui.text("mode")
                else:
                    column-=1
                    clicked, self.drop_downs[column][1] = imgui.combo(
                        self.drop_downs[column][0], self.drop_downs[column][1], modes)
                    self.drop_downs[column][2].data_manager.mode = modes[self.drop_downs[column][1]]

            elif row==2:
                if column==0:
                    imgui.text("xyz")
                else:
                    column-=1
                    clicked, self.xyz_axes[column][1] = imgui.combo(
                        self.xyz_axes[column][0], self.xyz_axes[column][1], xyz)
                    self.xyz_axes[column][2].show_axes = not xy2[self.xyz_axes[column][1]]

            elif row==3:
                if column==0:
                    imgui.text("data")
                else:
                    column -= 1
                    clicked, self.data_shown[column][1] = imgui.combo(
                        self.data_shown[column][0], self.data_shown[column][1], data_shown_types)
                    self.data_shown[column][2] = data_shown_types[self.data_shown[column][1]]



            if column == 0:
                #imgui.separator()
                pass
            

        imgui.separator()
        num_columns = 3
        n_data = 0
        num_rows = 4+n_data

        with imgui.begin_table("test", num_columns, imgui.TABLE_BORDERS_INNER_VERTICAL):
            imgui.table_setup_column("item", imgui.TABLE_COLUMN_WIDTH_FIXED)
            imgui.table_setup_column("a", imgui.TABLE_COLUMN_WIDTH_FIXED)
            imgui.table_setup_column("b", imgui.TABLE_COLUMN_WIDTH_FIXED)
            for r in range(num_rows):
                imgui.table_next_row()
                for c in range(num_columns):
                    imgui.table_set_column_index(c)

                    set_static_choices(r, c)

                    

        self.space_lines(4)
        self.space_lines(4)
        
        def set_data_choices(row, column):

            len_info = [len(self.point_info[0]), len(self.point_info[1])]

            if self.data_shown[column//2][-1] == 'newest':
                if row==len_info[column//2]-1: # -1 to zero index it
                    self.checked_data[column//2][row-1] = True
                else:
                    self.checked_data[column//2][row-1] = False

            if row-1<=len_info[column//2]:
                if c%2==0: # checkbox
                    _, self.checked_data[column//2][row-1] = imgui.checkbox(
                        f"##{row}{column}", self.checked_data[column//2][row-1])
                else: # point info
                    imgui.text(f'{self.point_info[column//2][row-1][-3]}')

                
            if any(self.checked_data[column//2]):
                i = max(i for i, v in enumerate(self.checked_data[column//2]) if v == True)
                impls[column//2].pt_selected = self.point_info[column//2][i]
            else:
                impls[column//2].pt_selected = None


            pass

        impls = [self.impl_a, self.impl_b]
        header = ['impl_a', 'point_a', 'impl_b', 'point_b']


        table_height = np.maximum(len(self.impl_a_checked), len(self.impl_b_checked))
        if table_height != 0:
            imgui.text("shown data points")
            imgui.separator()
        with imgui.begin_table("data_points", len(header), imgui.TABLE_BORDERS_INNER_VERTICAL):
            imgui.table_setup_column("d_a", imgui.TABLE_COLUMN_WIDTH_FIXED)
            imgui.table_setup_column("ip_b", imgui.TABLE_COLUMN_WIDTH_FIXED)
            imgui.table_setup_column("d_b", imgui.TABLE_COLUMN_WIDTH_FIXED)
            imgui.table_setup_column("ip_b", imgui.TABLE_COLUMN_WIDTH_FIXED)
            for r in range(table_height):
                imgui.table_next_row()
                for c in range(len(header)):
                    imgui.table_set_column_index(c)

                    if r==0:
                        imgui.text(header[c])
                    else:
                        set_data_choices(r, c)


        imgui.end()

        end = time.time()
        self.dt = end-self.current
        self.current = end


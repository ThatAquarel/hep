
        imgui.text("data points")
        imgui.separator()
        
        if self.impl_a_checked != []:
            if self.data_shown[0][2]=='newest':
                for i in range(len(self.impl_a_checked)):
                    self.impl_a_checked[i] = False
                self.impl_a_checked[-1] = True
        if self.impl_b_checked != []:
            if self.data_shown[0][2]=='newest':
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
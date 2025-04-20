    # NOTE : these use the old self.test format for data from the old data_manager.py
    # NOTE : now, one manager for impl a and b is used, with different function names
    # NOTE : thus, the below code won't work immediately if uncommented
    # def on_click(self, window):
    #     # get 3D click coordinates
    #     rh = self.get_right_handed()
    #     self.x, self.y, self.z = self.get_click_point(window, rh)
        
    #     print(self.x, self.y, self.z)
    #     uncertainty = 1
    #     for i in range(len(self.test.data)):
    #         #To see if the mouse position matches 
    #         if self.ui.dataset_active[i]:
    #             for pt in range(len(self.test.data[i])):     #test.data -> datasets -> cubes -> vertices or fan -> coords -> xyz values
    #                 if (self.test.data[i][pt][0][0][0] <= (self.x + uncertainty)) and (self.test.data[i][pt][0][0][0] >= (self.x - uncertainty)):
    #                     if (self.test.data[i][pt][0][0][1] <= (self.y + uncertainty)) and (self.test.data[i][pt][0][0][1] >= (self.y - uncertainty)):
    #                         self.pt_selected = self.test.data[i][pt]

from detection import *

class test:
    def __init__(self):
        detection_algorithm = Detection()
        self.data = []
        self.reset()

        self.testing()  #For real data, remove this line
        


    def has_data(self):
        pass
    
    def reset(self):
        """
        Reset Aljoscha's code, since we use different values
        """

        # Global variables
        detection_algorithm.level_count = 1
        detection_algorithm.n = 2*60 * 0.1 # Sideview length of scintillator in unit x


        # These values are used for x perspective
        detection_algorithm.upper_side_views = [(0, detection_algorithm.n)] # (start, end) coordinates for each level 
        detection_algorithm.lower_side_views = [(0, detection_algorithm.n)]

        detection_algorithm.plate_thickness = 10 * 0.1# In unit x
        detection_algorithm.intra_level_gap = 2 * 0.1#Actual physical gap between each level, in unit x
        detection_algorithm.inter_level_gap = detection_algorithm.plate_thickness + detection_algorithm.intra_level_gap # Adjusted inter level gap for computation 

        detection_algorithm.half_gap_size =  162/2 * 0.1# In unit x
        detection_algorithm.top_half_gap = detection_algorithm.half_gap_size + detection_algorithm.plate_thickness + detection_algorithm.intra_level_gap
        detection_algorithm.bottom_half_gap = detection_algorithm.half_gap_size
        detection_algorithm.gap_line = 0
        detection_algorithm.highest_point = detection_algorithm.half_gap_size + 5*detection_algorithm.intra_level_gap + 6*detection_algorithm.plate_thickness # Values custom set to this detector
        detection_algorithm.lowest_point = -detection_algorithm.highest_point

    def update_data(self,raw_data):
        """
        transform data ready to be interpreted by the visualizer, then update self.data
        """
    
        
        cooked_data = self.interpret_raw_data(raw_data)
        algorithmized = detection_algorithm.scintillators_to_bounds(cooked_data)

        self.reset()

        new_hull_bounds = self.transform_coordinates(algorithmized[0])
        new_fan_out_lines = self.transform_coordinates_fanned(algorithmized[1])

        #This part depends on if you want to make the point to be assigned to a dataset or as a new dataset
        point = [new_hull_bounds, new_fan_out_lines, cooked_data]
        dataset = []
        dataset.append(point)

        self.data.append(dataset)

    def interpret_raw_data(self,bin):
        x = bin & 3355443   #& operator on 0b001100110011001100110011
        y = bin & 13421772  #& operator on 0b110011001100110011001100

        bit = 12
        list_x = []
        list_y = []
        for i in range(0, bit, 2):
            last_two_x = (x >> (i * 2))
            list_x.append(((last_two_x & 2) >> 1, last_two_x & 1))

            last_two_x = (y >> (i * 2 + 2))
            list_y.append(((last_two_x & 2) >> 1, last_two_x & 1))

        return [list_x,list_y]
    
        #transforming coordinates
    def transform_coordinates(self,data):
        """
        transform into my coordinate system
        """
        translate_x = -detection_algorithm.n / 2
        translate_y = -detection_algorithm.n/2
        z_scale = 1

        list = []
        for coordinates in data:
            x = (coordinates[0] + translate_x) * -1
            y = (coordinates[1] + translate_y) * 1
            z = (coordinates[2] + detection_algorithm.half_gap_size - detection_algorithm.inter_level_gap + detection_algorithm.plate_thickness) / z_scale
            list.append((x,y,z))

        return list

    def transform_coordinates_fanned(self,data):
        list = []
        for pair in data:
            list.append(self.transform_coordinates(pair))

        return list
    

    def testing(self):
        scintillator_1= [[(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)],[(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)]]
        scintillator_2 = [[(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)], [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)]]
        
        self.update_data(0b101101010101101011010110)     



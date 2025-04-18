#import arduino

'''

Algorithm that takes in which scintillators lit up and returns a convex hull to bound the muon path

Input type : List containing tuples representing the activation states of each level from top to bottom
                     (0, 1) means every second scintillator lights up
                     (1, 0) means every first scintillator lights up
                     (1, 1) All the scintillator lit up
                     (0, 0) No scintillator lit up
            -- > See display software, contains a function that converts the 32 bit number 
                 that the detector outputs to the above formatting

Output type: Prism vertices and 2 points per fan out line
Current output type : For the moment 2 lines creating 

UPCOMING CHANGES : (In order of importance)
- Take advantage of (1, 1) type levels
- Write code in a class to permit scailability
- Efficiency review, current code is O(n), but all cases could be simulated and stored for lookup for O(log(n))

'''   

# Global variables
level_count = 1
n = 2*1 # Sideview length of scintillator in unit x


# These values are used for x perspective
upper_side_views = [(0, n)] # (start, end) coordinates for each level 
lower_side_views = [(0, n)]
half_gap_size = 0.5 # In unit x
plate_thickness = 0.2 # In unit x
inter_level_gap = 0.2 #2*1 + plate_thickness # In unit x, level gap*2 + y_plate thickness
gap_line = 0
highest_point = half_gap_size + 5*inter_level_gap + 6*plate_thickness # Values custom set to this detector
lowest_point = -highest_point

def update_perspective_values():
    global upper_side_views
    global lower_side_views
    global half_gap_size
    global inter_level_gap
    global gap_line
    global level_count
    global top_half_gap
    global bottom_half_gap

    upper_side_views = [(0, n)] # (start, end) coordinates for each level 
    lower_side_views = [(0, n)]

    top_half_gap = half_gap_size
    bottom_half_gap = half_gap_size + plate_thickness + intra_level_gap

    # Update level count
    level_count = 1


# Functions
def find_intersection(line1, line2):
    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2

    # Calculate the determinants
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:  # Lines are parallel
        return (-100, -100) #Point out of the detector

    x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
    y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

    return (x, y)


def find_points_on_line(line, target_y):
    '''
    Takes in a line and computes 2 points on the line for the line coordinate.
    '''
    x1, y1 = line[0]
    x2, y2 = line[1]

    # Find the x-coordinate for the given target y-coordinate
    def find_x_for_y(y):
        # Using the line equation: y - y1 = m(x - x1) -> solving for x
        return x1 + (y - y1) / m
    
    if x1 != x2: # Avoid division by zero
        # Calculate the slope (m)
        m = (y2 - y1) / (x2 - x1)

        # Find the x-coordinates for the target_y and -target_y
        x_pos = find_x_for_y(target_y)
        x_neg = find_x_for_y(-target_y)
    else : # If vertical line
        x_pos = x1
        x_neg = x2
    
    # Return the points
    return (x_pos, x_neg)




def hull_coordinates(x_bound, z_bound):
    '''
    Returns the 8 points that bound the rectangular prism (which is extended up in the rendering)
    [((0, 10), (0.25, -9)), ((0.25, 9), (0.5 -10))]
    '''
    global highest_point
    global lowest_point

    x_left_bound = x_bound[0]
    x_right_bound = x_bound[1]
    z_left_bound = z_bound[0]
    z_right_bound = z_bound[1]

    # Recalculate bounds for another y value
    x_left_bound = find_points_on_line(x_left_bound, highest_point)
    x_right_bound = find_points_on_line(x_right_bound, highest_point)
    z_left_bound = find_points_on_line(z_left_bound, highest_point)
    z_right_bound = find_points_on_line(z_right_bound, highest_point)

    # Match correspongind bounds (x, z, y) 
    bounding_points = [(x_left_bound[0], z_right_bound[0], highest_point), (x_left_bound[0], z_left_bound[0], highest_point),
                       (x_right_bound[0], z_right_bound[0], highest_point), (x_right_bound[0], z_left_bound[0], highest_point),
                       (x_left_bound[1], z_right_bound[1], lowest_point), (x_left_bound[1], z_left_bound[1], lowest_point),
                       (x_right_bound[1], z_right_bound[1], lowest_point), (x_right_bound[1], z_left_bound[1], lowest_point)]
    
    fan_out_points = [(bounding_points[0], bounding_points[-1]), (bounding_points[1], bounding_points[-2]),
                      (bounding_points[2], bounding_points[-3]), (bounding_points[3], bounding_points[-4])]
    
    return bounding_points, fan_out_points

def group_corresponding_levels(levels):
    '''
    Reorders the initial list of scintillators 
    '''
    # Group first with last, second with second to last, etc
    k = len(levels)
    grouped_levels = []
    
    # Pair up levels from outside moving inward
    for i in range(k // 2):
        grouped_levels.append((levels[i], levels[k-1-i]))
        
    return grouped_levels[::-1] # Put the elements in the middle first and the ones on the edges last


def draw_bounds(level_pair, previous_bounds):
    '''
    Takes the scintillators that were activated at corresponding levels and draws better bounds 
    according to previous bounds. 
    :param previous_bounds: 4 points, 2 points per old tightest line.
                            ((p1, p2), (p3, p4)) where (left_bound, right_bound)
    :return new_bounds: 4 points, 2 points per new tightest line. 
    '''

    # Will implement a version with classes to avoid this horror :
    global level_count
    global n
    global upper_side_views
    global lower_side_views
    global half_gap_size
    global plate_thickness
    global inter_level_gap
    global gap_line
    global top_half_gap
    global bottom_half_gap
    # Default point (0, n)
    # Ajusted point (side_view[level_count-1][0], side_view[level_count-1][1])

    upper_level = level_pair[0]
    lower_level = level_pair[1]

    upper_level_points = []
    lower_level_points = []
    
    # Adjust upper side view points
    interval = n / 2**level_count

    if upper_level == (1, 0):
        upper_side_views.append((upper_side_views[level_count-1][0], upper_side_views[level_count-1][0]+interval))
    elif upper_level == (0, 1):
        upper_side_views.append((upper_side_views[level_count-1][1]-interval, upper_side_views[level_count-1][1]))
    elif upper_level == (1, 1):
        # An implementation of this case will be made later to take full advantage of this unique situation
        return previous_bounds
        
    else :
        return None

    # Adjust lower side view points
    if lower_level == (1, 0):
        lower_side_views.append((lower_side_views[level_count-1][0], lower_side_views[level_count-1][0] + interval ))
    elif lower_level == (0, 1):
        lower_side_views.append((lower_side_views[level_count-1][1]-interval, lower_side_views[level_count-1][1]))
    elif lower_level == (1, 1):
        # An implementation of this case will be made later to take full advantage of this unique situation
        return previous_bounds
        
    else :
        return None
        
    
    # Increase counters
    level_count += 1

    # Set coordinate points for the rod on each level 
    upper_level_points.extend([(upper_side_views[level_count-1][0], top_half_gap + plate_thickness*(level_count-2) + inter_level_gap*(level_count-2)), # Lower left point
                                  (upper_side_views[level_count-1][1], top_half_gap + plate_thickness*(level_count-2) + inter_level_gap*(level_count-2)), # Lower right point
                                  (upper_side_views[level_count-1][0], top_half_gap + plate_thickness*(level_count-1) + inter_level_gap*(level_count-2)), # Upper left point
                                  (upper_side_views[level_count-1][1], top_half_gap + plate_thickness*(level_count-1) + inter_level_gap*(level_count-2))]) # Upper right point
    
    lower_level_points.extend([(lower_side_views[level_count-1][0], -(bottom_half_gap + plate_thickness*(level_count-2) + inter_level_gap*(level_count-2))), # Upper left point
                                  (lower_side_views[level_count-1][1], -(bottom_half_gap + plate_thickness*(level_count-2) + inter_level_gap*(level_count-2))), # Upper right point
                                  (lower_side_views[level_count-1][0], -(bottom_half_gap + plate_thickness*(level_count-1) + inter_level_gap*(level_count-2))), # Lower left point
                                  (lower_side_views[level_count-1][1], -(bottom_half_gap + plate_thickness*(level_count-1) + inter_level_gap*(level_count-2)))]) # Lower right point


    # Create level lines $ DPONT FORGET THIS
    upper_line_y = top_half_gap + (inter_level_gap+plate_thickness)*(level_count-2)
    lower_line_y = bottom_half_gap + (inter_level_gap+plate_thickness)*(level_count-2)
    upper_line = ((0, upper_line_y), (1, upper_line_y))
    lower_line = ((0, -lower_line_y), (1, -lower_line_y))

    # Create new potential lines
    left_bound = (upper_level_points[2], lower_level_points[2])
    right_bound = (upper_level_points[3], lower_level_points[3])

# Check if bounds are valid 
# Check this section it seems to mess things up
    # Check left_bound potential line intersections
    x, y = find_intersection(left_bound, previous_bounds[0])

    if left_bound[0][0] < x < left_bound[1][0]: # Check for intersection with a previous bound
        if y >= 0 : # Check gap side
            # print('Left upper previous bound intersection')
            left_bound = (previous_bounds[0][0], left_bound[1])
        else :
            # print('Left lower previous bound intersection')
            left_bound = (left_bound[0], previous_bounds[0][1])
    # Check left_bound potential scintillator non-valid overlap
    else:
        x, y = find_intersection(left_bound, upper_line)
        if not upper_level_points[0][0] < x < upper_level_points[1][0]:
            # print('detector line intersection upper left')
            left_bound = (upper_level_points[0], left_bound[1])

        x, y = find_intersection(left_bound, lower_line)
        if not lower_level_points[0][0] < x < lower_level_points[1][0]:
            # print('detector line intersection lower left')
            left_bound = (left_bound[0], lower_level_points[0])

    # Check right_bound potential line intersections

    x, y = find_intersection(right_bound, previous_bounds[1])
    if right_bound[0][0] < x < right_bound[1][0]: # Check for intersection with a previous bound
        if y >= 0 : # Check gap side
            # print('Right upper previous bound intersection')
            right_bound = (previous_bounds[1][0], right_bound[1])
        else :
            # print('Right lower previous bound intersection')
            right_bound = (right_bound[0], previous_bounds[1][1])
    # Check right_bound potential scintillator non-valid overlap
    else:
        x, y = find_intersection(right_bound, upper_line)
        if not upper_level_points[0][0] < x < upper_level_points[1][0]:
            # print('detector line intersection upper right')
            right_bound = (upper_level_points[1], right_bound[1])

        x, y = find_intersection(right_bound, lower_line)
        if not lower_level_points[0][0] < x < lower_level_points[1][0]:
            # print('detector line intersection lower right')
            right_bound = (right_bound[0], lower_level_points[1])

    return [left_bound, right_bound]



###############################

def scintillators_to_bounds(binary):
    '''
    :param scintillators: tuple containing two lists, one for each side view
    :return bounds: tuple containing two lists each containing the points that bound the muon path
    '''
    scintillators = interpret_raw_data(binary)

    x_view = scintillators[0]
    z_view = scintillators[1]

    x_bounds = detect_side_view(x_view)
    update_perspective_values()
    z_bounds = detect_side_view(z_view)

    if x_bounds == None or z_bounds == None:
        return None

    hull_bounds, fan_out_lines = hull_coordinates(x_bounds, z_bounds)
    
    print(hull_bounds)

        #coordinate transformation
    hull_bounds = transform_coordinates(hull_bounds)
    fan_out_lines = transform_coordinates_fanned(fan_out_lines)

    
    #condensed for clicking feature
    bin6 = bit8(binary)

    return hull_bounds, fan_out_lines, bin6


#Raw data to normal data
def bit8(var):
    bit8 = 0
    for i in range(0, 12):

        new = (var >> 2 * i)&3

        if  new == 2:

            bit8 += 2**i

        elif new != 1:

            return False
        
    return bit8

def bin_to_list(bin):
    bit = 12      
    list = []
    for i in range(bit//2):

        first_two  = (bin >> ((bit-2) - 2 * i)) & 3

        if first_two == 2:

            list.append((1,0))

        elif first_two == 1:

            list.append((0,1))

        elif first_two == 3:

            list.append((1,1))
        
        else:
            return False    #error
    
    return list

def interpret_raw_data(bin):
    x = bin & 3355443   #& operator on 0b001100110011001100110011
    y = bin & 13421772  #& operator on 0b110011001100110011001100

    bit = 12
    bitminus2 = bit - 2
    list_x = []
    list_y = []
    for i in range(0, bit, 2):
        last_two_x = (x >> (i * 2))
        list_x.append(((last_two_x & 2) >> 1, last_two_x & 1))

        last_two_x = (y >> (i * 2 + 2))
        list_y.append(((last_two_x & 2) >> 1, last_two_x & 1))

    return [list_x,list_y]



#transforming coordinates
def transform_coordinates(data):
    global n      #scale
    global half_gap_size
    global inter_level_gap

    translate_x = -n / 2
    translate_y = -n / 2
    z_scale = 1

    list = []
    for coordinates in data:
        x = (coordinates[0] + translate_x) * -1
        y = (coordinates[1] + translate_y) * -1
        z = (coordinates[2] + half_gap_size - inter_level_gap) / z_scale
        list.append((x,y,z))

    return list

def transform_coordinates_fanned(data):
    list = []
    for pair in data:
        list.append(transform_coordinates(pair))

    return list

#run this loop to call arduino to update data
def update_data():
    global data

    add_data = []
    packet = arduino.recv_packet(arduino.ser)

    add_data.append(scintillators_to_bounds(packet))    #This creates a new dataset (check description)

    data.append(add_data)


#test.data -> datasets -> cubes -> vertices or fan -> coords -> xyz values


data_all = []
# data1 = interpret_raw_data(0b101010101010101010101010)
# data2 = interpret_raw_data(0b010101010101010101010101)

data_all.append(scintillators_to_bounds(0b101010101010101010101010))    #problem with 0b100110101010101010101010
data_all.append(scintillators_to_bounds(0b010101010101010101010101))


data = []
data.append(data_all)




# def coordinates(binary):
#     scintillators = interpret_raw_data(binary&16773120)

#     x = (bit8(scintillators[0]) -8) /8
#     y = (bit8(scintillators[1]) - 8) /8
#     z = 0

#     dx = 0.0625
#     dy = 0.0625
#     dz = 0.0625

#     p1 = (x + dx, y + dy,z + dz)
#     p2 = (x + dx, y - dy,z + dz)
#     p3 = (x - dx, y + dy,z + dz)
#     p4 = (x - dx, y - dy,z + dz)
#     p5 = (x + dx, y + dy,z - dz)
#     p6 = (x + dx, y - dy,z - dz)
#     p7 = (x - dx, y + dy,z - dz)
#     p8 = (x - dx, y - dy,z - dz)

#     bin6 = bit8(binary)
#     return [p1,p2,p3,p4,p5,p6,p7,p8],[[p1,p8],[p2,p7],[p3,p6],[p4,p5]], bin6

#[data] = dataset

#print(scintillators_to_bounds(data))

# if __name__ == '__main__':


    # scintillators = [(1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1)]
    # best_path = detect_side_view(scintillators)
    # print(f'The path is bounded by {best_path}')


    # Example test cases: scintillators = [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1)] ---> Pass
                          # >> [((0, 10), (0.25, -9)), ((0.25, 9), (0.5 -10))]
    # [(0, 1), (1, 0), (1, 0), (1, 0), (0, 1), (1, 0)] ---> Pass 
                          # >> [((0.25, 10), (0.5, -7)), ((0.5, 7), (0.75, -10))]
    # [(1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1)] ---> Pass
                          # >> [((0.5, 10), (1.25, -9)), ((0.75, 9), (1.5, -10)) 


# scintillators = [(1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1)]
# best_path = detect_side_view(scintillators)
# print(f'The path is bounded by {best_path}')
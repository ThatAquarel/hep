# ---------   Cartesian rod pattern simulation ------- #
# To implement : probability simulation for unkown path

import random
import math


def level_generator(level_n):
    """
    Generates a list of lists of boundaries modeling the area enclosed
    by the rods
    Distance units in this code are millimeters
    X and Y boundaries are treated differently to allow for different x y values
    The first level is 0
    :param level_n: Indicates what level of the structure
                    is being generated. Is used to generate the shift between
                    levels
    """

    # Confirm below values o brave bromont skier
    rod_width = 5
    rod_heigth = 2000  # Make generation simpler for now by avoiding several rows on the same level
    spacing = 5
    shift = 0.5
    level_shift = shift * math.floor(level_n / 2)

    # Boundary equation for surface to cover
    x_pos_boundary = 2000
    x_neg_boundary = 0
    y_pos_boundary = 2000
    y_neg_boundary = 0

    # Determine level type (Where x is True)
    x_lvl = True if (level_n % 2 == 0) else False

    # Number of rods
    n_rods_x = int((x_pos_boundary - x_neg_boundary) / (rod_width + spacing))
    n_rods_y = int((x_pos_boundary - x_neg_boundary) / (rod_width + spacing))
    lvl_rods = n_rods_x if x_lvl else n_rods_y

    # Check for redundant shifting
    if rod_width < level_shift:
        raise Exception(
            f"Superflous shifting {level_n} is overlapping with a previous level"
        )

    # Store generated rods in a list of lists
    level = []

    # Generate rods
    for iterations, delayed_iteration in enumerate(range(lvl_rods), 1):
        if x_lvl:
            rod_upper_x_boundary = (
                x_neg_boundary
                + rod_width * iterations
                + spacing * delayed_iteration
                + level_shift
            )
            rod_lower_x_boundary = (
                x_neg_boundary
                + rod_width * delayed_iteration
                + spacing * delayed_iteration
                + level_shift
            )
            if rod_upper_x_boundary <= x_pos_boundary:
                level.append([rod_lower_x_boundary, rod_upper_x_boundary])
        else:
            rod_upper_y_boundary = (
                y_neg_boundary
                + rod_width * iterations
                + spacing * delayed_iteration
                + level_shift
            )
            rod_lower_y_boundary = (
                y_neg_boundary
                + rod_width * delayed_iteration
                + spacing * delayed_iteration
                + level_shift
            )
            if rod_upper_y_boundary <= y_pos_boundary:
                level.append([rod_lower_y_boundary, rod_upper_y_boundary])

    return level


def trajectory_generator():
    """
    This function generates a point for muon trajectory
    """
    x = (
        random.randint(0, 2_000_000) / 1000
    )  # Get a very small trajectory to approximate muon
    y = random.randint(0, 2_000_000) / 1000

    return x, y


def detector_generator(level_amount):
    """
    This functions returns all the levels making up the detector
    :param level_amount: Amount of levels in the detector
    """
    detector = []
    for level in range(level_amount):
        detector.append(level_generator(level))

    return detector


def check_detector(detector, trajectory_x, trajectory_y):
    """
    Returns the detectors best guess for the muon position
    """

    estimate_x = [0, 2000]
    estimate_y = [0, 2000]

    for level_n, level_rods in enumerate(detector):
        if (level_n % 2) == 0:  # Check x levels
            for rod in level_rods:
                if rod[0] < trajectory_x < rod[1]:  # Check if muons is in bounds
                    if rod[0] > estimate_x[0]:  # Check if current guess can be refined
                        estimate_x[0] = rod[0]
                    if rod[1] < estimate_x[1]:
                        estimate_x[1] = rod[1]
                    break
        else:  # Check for y levels
            for rod in level_rods:
                if rod[0] < trajectory_y < rod[1]:  # Check if muons is in bounds
                    if rod[0] > estimate_y[0]:  # Check if current guess can be refined
                        estimate_y[0] = rod[0]
                    if rod[1] < estimate_y[1]:
                        estimate_y[1] = rod[1]
                    break

    return estimate_x, estimate_y


def simulation(muons=10_000):
    """
    Test detector precision for amount of muons
    """
    detector = detector_generator(22)
    muon_areas = []

    for _ in range(muons):
        trajectory_x, trajectory_y = trajectory_generator()
        estimate_x, estimate_y = check_detector(detector, trajectory_x, trajectory_y)

        muon_area = (estimate_y[1] - estimate_y[0]) * (
            estimate_x[1] - estimate_x[0]
        )  # Size of the area where the muon could be
        muon_areas.append(muon_area)

    avg_muon_area = sum(muon_areas) / len(muon_areas)
    print(
        f"The detector can on average locate a muon in a {avg_muon_area} mm2 rectangle."
    )


if __name__ == "__main__":
    simulation()

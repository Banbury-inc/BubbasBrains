
import math

def calculate_wheel_parameters(s, x, y, wheel_base_width=31, wheel_base_length=48):
    # Initialize variables
    lfa = lra = rfa = rra = lfr = lrr = rfr = rrr = 0
    travel_radius = lfs = lrs = rfs = rrs = 0
    lfd = lrd = rfd = rrd = 0

    # Turning radius of tractor
    if x == 0 and abs(y) > wheel_base_length / 2:
        travel_radius = 0
    else:
        travel_radius = math.sqrt(x ** 2 + y ** 2)

    # Calculate left front
    if x == 0 and abs(y) > wheel_base_length / 2:
        lfa = 90  # Wheel angle
        lfs = s   # Wheel speed
        lfd = 1 if y > 0 else 0  # Wheel direction
    else:
        # Wheel angle
        lfr = math.sqrt((x - wheel_base_width / 2) ** 2 + (y - wheel_base_length / 2) ** 2)
        lfa = 90 - (math.atan((x - wheel_base_width / 2) / (y - wheel_base_length / 2)) * 180 / math.pi)
        if x < 0 and y > 0:
            lfa -= 90
        lfa = lfa + 90 if lfa < 90 else lfa - 90

        # Wheel speed
        lfs = s * (lfr / travel_radius) if s != 0 else 0

        # Wheel direction
        lfd = 1 if x < wheel_base_width / 2 and y < wheel_base_length / 2 else 0

    # Calculate right front
    if x == 0 and abs(y) > wheel_base_length / 2:
        rfa = 90  # Wheel angle
        rfs = s   # Wheel speed
        rfd = 0 if y > 0 else 1  # Wheel direction
    else:
        # Wheel angle
        rfr = math.sqrt((x + wheel_base_width / 2) ** 2 + (y - wheel_base_length / 2) ** 2)
        rfa = 90 - (math.atan((x + wheel_base_width / 2) / (y - wheel_base_length / 2)) * 180 / math.pi)
        if x < 0 and y > 0:
            rfa -= 90
        rfa = rfa + 90 if rfa < 90 else rfa - 90

        # Wheel speed
        rfs = s * (rfr / travel_radius) if s != 0 else 0

        # Wheel direction
        rfd = 0 if x < wheel_base_width / 2 and y < wheel_base_length / 2 else 1

    # Return calculated parameters
    return (lfa, lra, rfa, rra, lfr, lrr, rfr, rrr, travel_radius, lfs, lrs, rfs, rrs, lfd, lrd, rfd, rrd)

def simulate():
    speed = int(input("Enter speed: "))
    x_coord = float(input("Enter x coordinate: "))
    y_coord = float(input("Enter y coordinate: "))
    wheel_params = calculate_wheel_parameters(speed, x_coord, y_coord)
    print("Wheel Parameters:", wheel_params)

# Test the function
simulate()

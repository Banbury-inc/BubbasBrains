import math

def get_steering_angle_and_speed(speed, x_coordinate, y_coordinate):
    wheel_base_width = 31  # 40 wheel base width in inches
    wheel_base_length = 48  # 43 wheel base length in inches

    # turning radius of tractor
    if x_coordinate == 0 and abs(y_coordinate) > wheel_base_length / 2:
        travel_radius = 0
    else:
        travel_radius = math.sqrt(x_coordinate ** 2 + y_coordinate ** 2)
    
    # calculate left front
    if x_coordinate == 0 and abs(y_coordinate) > wheel_base_length / 2:
        lfa = 90  # wheel angle
        lfs = speed  # wheel speed
        lfd = 1 if y_coordinate > 0 else 0  # wheel direction
    else:
        # wheel angle
        lfr = math.sqrt((x_coordinate - wheel_base_width / 2) ** 2 + (y_coordinate - wheel_base_length / 2) ** 2)
        lfa = 90 - (math.atan((x_coordinate - wheel_base_width / 2) / (y_coordinate - wheel_base_length / 2)) * 180 / math.pi)
        if x_coordinate < 0 and y_coordinate > 0:
            lfa -= 90
        lfa = lfa + 90 if lfa < 90 else lfa - 90

        # wheel speed
        lfs = speed * (lfr / travel_radius) if speed != 0 else 0

        # wheel direction
        lfd = 1 if x_coordinate < wheel_base_width / 2 and y_coordinate < wheel_base_length / 2 else 0

    # calculate right front
    if x_coordinate == 0 and abs(y_coordinate) > wheel_base_length / 2:
        rfa = 90  # wheel angle
        rfs = speed  # wheel speed
        rfd = 0 if y_coordinate > 0 else 1  # wheel direction
    else:
        # wheel angle
        rfr = math.sqrt((x_coordinate + wheel_base_width / 2) ** 2 + (y_coordinate - wheel_base_length / 2) ** 2)
        rfa = 90 - (math.atan((x_coordinate + wheel_base_width / 2) / (y_coordinate - wheel_base_length / 2)) * 180 / math.pi)
        if x_coordinate < 0 and y_coordinate > 0:
            rfa -= 90
        rfa = rfa + 90 if rfa < 90 else rfa - 90

        # wheel speed
        rfs = speed * (rfr / travel_radius) if speed != 0 else 0

        # wheel direction
        rfd = 0 if x_coordinate < wheel_base_width / 2 and y_coordinate < wheel_base_length / 2 else 1
    return lfs, lfa, lfd, rfs, rfa, rfd

def main():
    speed = int(input("Enter a speed: "))
    x_coordinate = int(input("Enter an x_coordinate: "))
    y_coordinate = int(input("Enter an y_coordinate: "))

    left_front_speed, left_front_angle, left_front_direction, right_front_speed, right_front_angle, right_front_directrion = get_steering_angle_and_speed(speed, x_coordinate, y_coordinate)
    print("Left front speed: ", left_front_speed)
    print("Left front angle: ", left_front_angle)
    print("Left front direction: ", left_front_direction)
    print("Right front speed: ", right_front_speed)
    print("Right front angle: ", right_front_angle)
    print("Right front direction: ", right_front_directrion)
if __name__ == "__main__":
    main()


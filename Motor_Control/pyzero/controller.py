import math
import tkinter as tk
import time
import threading

class VirtualLever:
    def __init__(self, root, max_speed=5):
        self.root = root
        self.max_speed = max_speed  # Define the maximum speed
        
        self.canvas = tk.Canvas(root, width=100, height=300)
        self.canvas.pack(side='left')

        # Draw the lever background
        self.lever_bg = self.canvas.create_rectangle(25, 25, 75, 275, fill="lightgrey")

        # Draw the lever (movable part)
        self.lever = self.canvas.create_rectangle(30, 130, 70, 170, fill="darkgrey")

        # Bind mouse events
        self.canvas.tag_bind(self.lever, "<ButtonPress-1>", self.on_click)
        self.canvas.tag_bind(self.lever, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.lever, "<ButtonRelease-1>", self.on_release)

        self.lever_position = 150  # Initial position in the middle
        self.current_speed = 0  # Initialize current speed
        self.update_speed()



    def on_click(self, event):
        self.canvas.tag_raise(self.lever)

    def on_drag(self, event):
        # Restrict the movement of the lever within the background
        new_y = min(max(event.y, 25), 275)  # Ensure the lever stays within the designated area
        self.canvas.coords(self.lever, 30, new_y - 20, 70, new_y + 20)
        self.lever_position = new_y
        self.update_speed()

    def on_release(self, event):
        self.update_speed()

    def update_speed(self):
        # Calculate the new speed based on the lever position
        # Assuming the top position corresponds to max speed and the bottom to 0
        self.current_speed = self.max_speed * (1 - ((self.lever_position - 25) / 250))


class VirtualJoystick:
    def __init__(self, root, lever):
        self.root = root
        self.root.title("Virtual Joystick")
        self.lever = lever 

        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()

        # Output display
        self.output_display = tk.Text(root, height=10, width=50)
        self.output_display.pack()


        # Draw outer circle (base of joystick)
        self.outer_circle = self.canvas.create_oval(50, 50, 250, 250, fill="gray")

        # Draw inner circle (movable joystick)
        self.inner_circle = self.canvas.create_oval(120, 120, 180, 180, fill="black")

        # Bind mouse events
        self.canvas.tag_bind(self.inner_circle, "<ButtonPress-1>", self.on_click)
        self.canvas.tag_bind(self.inner_circle, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.inner_circle, "<ButtonRelease-1>", self.on_release)

        self.joystick_position = (0, 0)
        self.inner_circle_center = (150, 150)  # Initial position at the center
        self.update_position()

    def on_click(self, event):
        self.canvas.tag_raise(self.inner_circle)
        self.inner_circle_center = (event.x, event.y)

    def on_drag(self, event):
        dx = event.x - self.inner_circle_center[0]
        dy = event.y - self.inner_circle_center[1]
        self.canvas.move(self.inner_circle, dx, dy)
        self.inner_circle_center = (event.x, event.y)
        self.update_position()

    def on_release(self, event):
        # Set the inner circle directly to the center position
        self.canvas.coords(self.inner_circle, 120, 120, 180, 180)
        self.inner_circle_center = (150, 150)
        self.joystick_position = (0, 0)
        self.update_position()

    def update_position(self):
        # Get the current position of the inner circle
        x1, y1, x2, y2 = self.canvas.coords(self.inner_circle)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        # Normalize the position based on the size of the outer circle
        self.joystick_position = ((center_x - 150) / 100, (150 - center_y) / 100)

        self.display_output()


    def display_output(self):
        # Calculate the angles and speeds based on the joystick position
        # speed = 1
        speed = self.lever.current_speed
        x_coordinate, y_coordinate = self.joystick_position
        left_front_speed, left_front_angle, left_front_direction, right_front_speed, right_front_angle, right_front_direction = get_steering_angle_and_speed(speed, x_coordinate, y_coordinate)

        # Clear the previous output
        self.output_display.delete('1.0', tk.END)

        # Display the new output
        output_text = f"""Joystick Position: {x_coordinate:.2f}, {y_coordinate:.2f}
        Left Front Speed: {left_front_speed:.2f}
        Left Front Angle: {left_front_angle:.2f}
        Left Front Direction: {left_front_direction}
        Right Front Speed: {right_front_speed:.2f}
        Right Front Angle: {right_front_angle:.2f}
        Right Front Direction: {right_front_direction}
        """
        self.output_display.insert(tk.END, output_text)

class JoystickApp:
    def __init__(self):
        self.root = tk.Tk()

        self.lever = VirtualLever(self.root)
        self.joystick = VirtualJoystick(self.root, self.lever)
        self.root.mainloop()



def get_steering_angle_and_speed(speed, x_coordinate, y_coordinate):
    wheel_base_width = 31  # 40 wheel base width in inches
    wheel_base_length = 48  # 43 wheel base length in inches

    # Check if the y-coordinate is zero
    if y_coordinate == 0:
        travel_radius = 0
    else:
        # turning radius of tractor
        if x_coordinate == 0 and abs(y_coordinate) > wheel_base_length / 2:
            travel_radius = 0
        else:
            travel_radius = math.sqrt(x_coordinate ** 2 + y_coordinate ** 2)
    
    # calculate left front
    if x_coordinate == 0 and abs(y_coordinate) > wheel_base_length / 2:
        left_front_angle = 90  # wheel angle
        left_front_speed = speed  # wheel speed
        left_front_direction = 1 if y_coordinate > 0 else 0  # wheel direction
        
    else:
        # wheel angle
        left_front_radius = math.sqrt((x_coordinate - wheel_base_width / 2) ** 2 + (y_coordinate - wheel_base_length / 2) ** 2)
        left_front_angle = 90 - (math.atan((x_coordinate - wheel_base_width / 2) / (y_coordinate - wheel_base_length / 2)) * 180 / math.pi)
        if x_coordinate < 0 and y_coordinate > 0:
            left_front_angle -= 90
        left_front_angle = left_front_angle + 90 if left_front_angle < 90 else left_front_angle - 90
        # wheel speed
        if travel_radius != 0:
            left_front_speed = speed * (left_front_radius / travel_radius)
        else:
            left_front_speed = 0
        # wheel direction
        left_front_direction = 1 if x_coordinate < wheel_base_width / 2 and y_coordinate < wheel_base_length / 2 else 0

    # calculate right front
    if x_coordinate == 0 and abs(y_coordinate) > wheel_base_length / 2:
        right_front_angle = 90  # wheel angle
        right_front_speed = speed  # wheel speed
        right_front_direction = 0 if y_coordinate > 0 else 1  # wheel direction
    else:
        # wheel angle
        right_front_radius = math.sqrt((x_coordinate + wheel_base_width / 2) ** 2 + (y_coordinate - wheel_base_length / 2) ** 2)
        right_front_angle = 90 - (math.atan((x_coordinate + wheel_base_width / 2) / (y_coordinate - wheel_base_length / 2)) * 180 / math.pi)
        if x_coordinate < 0 and y_coordinate > 0:
            right_front_angle -= 90
        right_front_angle = right_front_angle + 90 if right_front_angle < 90 else right_front_angle - 90
        # wheel speed
        if travel_radius != 0:
            right_front_speed = speed * (right_front_radius / travel_radius)
        else:
            right_front_speed = 0
        # wheel direction
        right_front_direction = 0 if x_coordinate < wheel_base_width / 2 and y_coordinate < wheel_base_length / 2 else 1

    return left_front_speed, left_front_angle, left_front_direction, right_front_speed, right_front_angle, right_front_direction

def print_angles(joystick_app):
    while True:
        x_coordinate, y_coordinate = joystick_app.joystick.joystick_position
        left_front_speed, left_front_angle, left_front_direction, right_front_speed, right_front_angle, right_front_directrion = get_steering_angle_and_speed(1, x_coordinate, y_coordinate)
        print(f"Joystick Position: {x_coordinate}, {y_coordinate}")
        print("Left front speed:", left_front_speed)
        print("Left front angle:", left_front_angle)
        print("Left front direction:", left_front_direction)
        print("Right front speed:", right_front_speed)
        print("Right front angle:", right_front_angle)
        print("Right front direction:", right_front_directrion)
        time.sleep(1)

def main():
    joystick_app = JoystickApp()
    update_thread = threading.Thread(target=print_angles, args=(joystick_app,))
    update_thread.daemon = True
    update_thread.start()
    joystick_app.root.mainloop()


if __name__ == "__main__":
    main()


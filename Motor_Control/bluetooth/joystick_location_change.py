import tkinter as tk
import threading
import bluetooth
import time

class VirtualJoystick:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Joystick")

        # Set the window to fullscreen
        self.root.attributes('-fullscreen', True)

        # Adjust the canvas size to fill the entire screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height)
        self.canvas.pack()

        # Dimensions and positions for the joystick
        self.radius = 100  # Radius for outer circle
        self.inner_radius = 30  # Radius for inner circle
        margin = 50  # Margin from the bottom and left edges of the screen

        # Draw outer circle (base of joystick) at the bottom-left corner
        self.outer_circle = self.canvas.create_oval(
            margin, screen_height - margin - 2*self.radius,
            margin + 2*self.radius, screen_height - margin, fill="gray")

        # Draw inner circle (movable joystick)
        self.inner_circle = self.canvas.create_oval(
            margin + self.radius - self.inner_radius, screen_height - margin - self.radius - self.inner_radius,
            margin + self.radius + self.inner_radius, screen_height - margin - self.radius + self.inner_radius, fill="black")

        # Initial position of the inner circle (center of the outer circle)
        self.inner_circle_center = (margin + self.radius, screen_height - margin - self.radius)
        self.initial_x, self.initial_y = self.inner_circle_center

        # Bind mouse events
        self.canvas.tag_bind(self.inner_circle, "<ButtonPress-1>", self.on_click)
        self.canvas.tag_bind(self.inner_circle, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.inner_circle, "<ButtonRelease-1>", self.on_release)

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
        # Snap back the inner circle to the initial center position
        self.canvas.coords(self.inner_circle,
                           self.initial_x - self.inner_radius, self.initial_y - self.inner_radius,
                           self.initial_x + self.inner_radius, self.initial_y + self.inner_radius)

    def update_position(self):
        # Get the current position of the inner circle
        x1, y1, x2, y2 = self.canvas.coords(self.inner_circle)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        # Normalize the position based on the size of the outer circle and screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        normalized_x = (center_x - 50) / (screen_width - 100)
        normalized_y = (screen_height - center_y - 50) / (screen_height - 100)
        self.joystick_position = (normalized_x, normalized_y)

root = tk.Tk()
joystick = VirtualJoystick(root)

try:
    root.mainloop()
except tk.TclError as e:
    print("Tkinter error:", e)


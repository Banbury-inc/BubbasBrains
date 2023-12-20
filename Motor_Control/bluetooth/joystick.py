import tkinter as tk
import time
import threading
import bluetooth


class VirtualJoystick:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Joystick")

        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()

        # Draw outer circle (base of joystick)
        self.outer_circle = self.canvas.create_oval(50, 50, 250, 250, fill="gray")

        # Draw inner circle (movable joystick)
        self.inner_circle = self.canvas.create_oval(120, 120, 180, 180, fill="black")

        # Bind mouse events
        self.canvas.tag_bind(self.inner_circle, "<ButtonPress-1>", self.on_click)
        self.canvas.tag_bind(self.inner_circle, "<B1-Motion>", self.on_drag)

        self.joystick_position = (0, 0)
        self.update_thread = threading.Thread(target=self.print_position)
        self.update_thread.daemon = True
        self.update_thread.start()

    def on_click(self, event):
        self.canvas.tag_raise(self.inner_circle)
        self.inner_circle_center = (event.x, event.y)

    def on_drag(self, event):
        dx = event.x - self.inner_circle_center[0]
        dy = event.y - self.inner_circle_center[1]
        self.canvas.move(self.inner_circle, dx, dy)
        self.inner_circle_center = (event.x, event.y)
        self.update_position()

    def update_position(self):
        # Get the current position of the inner circle
        x1, y1, x2, y2 = self.canvas.coords(self.inner_circle)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        # Normalize the position based on the size of the outer circle
        self.joystick_position = ((center_x - 150) / 100, (center_y - 150) / 100)

    def print_position(self):
        while True:
            print(f"Joystick Position: {self.joystick_position}")
            time.sleep(1)

root = tk.Tk()
joystick = VirtualJoystick(root)
root.mainloop()

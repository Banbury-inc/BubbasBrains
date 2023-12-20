
import tkinter as tk
import threading
import bluetooth
import time

class VirtualJoystick:
    def __init__(self, root, raspberry_pi_address):
        self.root = root
        self.root.title("Virtual Joystick")

        # Bluetooth setup
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((raspberry_pi_address, 1))
        self.stop_event = threading.Event()

        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()

        # Draw outer and inner circles
        self.outer_circle = self.canvas.create_oval(50, 50, 250, 250, fill="gray")
        self.inner_circle = self.canvas.create_oval(120, 120, 180, 180, fill="black")

        # Bind mouse events
        self.canvas.tag_bind(self.inner_circle, "<ButtonPress-1>", self.on_click)
        self.canvas.tag_bind(self.inner_circle, "<B1-Motion>", self.on_drag)

        self.joystick_position = (0, 0)

        # Start the update thread
        self.update_thread = threading.Thread(target=self.send_position)
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
        x1, y1, x2, y2 = self.canvas.coords(self.inner_circle)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        self.joystick_position = ((center_x - 150) / 100, (center_y - 150) / 100)

    def send_position(self):
        while not self.stop_event.is_set():
            try:
                position_str = f"{self.joystick_position[0]:.2f},{self.joystick_position[1]:.2f}"
                self.sock.send(position_str)
            except bluetooth.btcommon.BluetoothError as e:
                print(f"Bluetooth Error: {e}")
                break
            time.sleep(1)

    def close(self):
        self.stop_event.set()
        self.update_thread.join()
        self.sock.close()

raspberry_pi_address = "E4:5F:01:FB:B2:F8"  # Replace with your Raspberry Pi's address

root = tk.Tk()
joystick = VirtualJoystick(root, raspberry_pi_address)

try:
    root.mainloop()
finally:
    joystick.close()

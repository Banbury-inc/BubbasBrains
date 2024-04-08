from evdev import InputDevice, categorize, ecodes

# Replace 'your_device_path' with the path to your controller device
device_path = '/dev/input/event18'  # Example path, replace with actual device path

# Open the device
dev = InputDevice(device_path)

print("Listening for events from", dev)

# Listen for events
for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        if key_event.keystate == key_event.key_down:
            print("Button pressed:", key_event.keycode)


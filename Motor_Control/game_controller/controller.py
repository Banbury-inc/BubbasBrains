import usb.core
import usb.util
import pygame
from inputs import devices, get_gamepad



'''
1 =  Key BTN_TRIGGER 1
2 =  Key BTN_THUMB 1
3 =  Key BTN_THUMB2 1
4 =  Key BTN_TOP 1
left joystick vertical value = Abolute ABS_Y_1   (0-255)   (number at the end is location of joystick )
left joystick horizontal value = Abolute ABS_X_1    (0-255)  (number at the end is location of joystick )
right joystick vertical value = Abolute ABS_RZ_1    (0-255)  (number at the end is location of joystick )
right joystick horizontal value = Abolute ABS_Z_1    (0-255)  (number at the end is location of joystick )
left dpad = Absolute ABS_HATOX -1
right dpad = Absolute ABS_HATOY -1
up dpad = Absolute ABS_HATOX 1
down dpad = Absolute ABS_HATOX 1
R1 = Key BTN_PINKIE 1
R2 = Key BTN_BASE2 1
L1 = Key BTN_TOP2 1
L2 = Key BTN_BASE 1
select = Key BTN_BASE3 1
start = Key BTN_BASE4 1

'''

def find_device(vendor_id, product_id):
    # Find the USB device
    device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
    if device is None:
        print("Device not found")
    else:
        print("Device found:")
        print("  ID Vendor : ID Product = {:04x}:{:04x}".format(device.idVendor, device.idProduct))

# Replace 'vendor_id' and 'product_id' with your device's vendor and product IDs
vendor_id = 0x0e8f  # Vendor ID for GreenAsia Inc.
product_id = 0x0008  # Product ID for PS(R) Gamepad

find_device(vendor_id, product_id)





# Initialize Pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

try:
    # Attempt to setup the joystick
    joystick = pygame.joystick.Joystick(0)  # Joystick number 0
    joystick.init()
    print("Joystick initialized: ", joystick.get_name())
except pygame.error:
    print("No joystick found.")

def read_gamepad():
    print("Gamepad:", devices.gamepads)
    if not devices.gamepads:
        print("No gamepad found.")
        return

    try:
        while True:
            events = get_gamepad()
            for event in events:
                print(event.ev_type, event.code, event.state)
    except KeyboardInterrupt:
        print("Stopped by user.")

read_gamepad()

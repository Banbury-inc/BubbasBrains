from adafruit_servokit import ServoKit
import time

# Initialize the ServoKit with the specified I2C bus and address
kit = ServoKit(channels=16)

# Define the function for gradual movement using fractions
def gradual_move_to_fraction(servo, target_fraction, step=0.01, delay=0.03):
    fraction = servo.fraction  # Start from the current fraction
    step = step if target_fraction > fraction else -step
    while (0.0 <= fraction <= 1.0) and ((fraction < target_fraction and step > 0) or (fraction > target_fraction and step < 0)):
        servo.fraction = fraction
        fraction += step
        # Ensure the fraction is within bounds
        if step > 0 and fraction > target_fraction:
            fraction = target_fraction
        if step < 0 and fraction < target_fraction:
            fraction = target_fraction
        time.sleep(delay)
    # Make sure to set the final position within the valid range
    servo.fraction = max(0.0, min(target_fraction, 1.0))

# Define a function for moving to a position fractionally
def move_to_position_fractionally(elbow_frac, wrist_frac, shoulder_frac, hand_frac):
    gradual_move_to_fraction(kit.servo[2], elbow_frac)    # Elbow
    gradual_move_to_fraction(kit.servo[3], wrist_frac)    # Wrist
    gradual_move_to_fraction(kit.servo[4], shoulder_frac) # Shoulder
    gradual_move_to_fraction(kit.servo[1], hand_frac)     # Hand

# Function for the pick-up sequence using fractional movement
def pick_up_object_fractionally():
    # First position - Approach (fractions are placeholders, set them to your requirements)
    move_to_position_fractionally(0.0, 0.5, 0.25, 0.7)
    
    # Second Position - Position above object
    move_to_position_fractionally(0.25, 0.5, 0.8, 0.7)
    
    # Third Position - Grab object
    move_to_position_fractionally(0.3, 0.5, 0.8, 0.9)
    
    # Fourth position - Lift object
    move_to_position_fractionally(0.1, 0.5, 0.25, 0.9)
    move_to_position_fractionally(0.8, 0.5, 0.25, 0.9)
    

try:
    # Perform the pick-up sequence using fractional movement
    pick_up_object_fractionally()
finally:
    # De-initialize the PCA9685 to turn off the servo drivers (if you're using a PCA9685-based driver)
    # If you want to deinitialize the entire PCA9685, you can call kit.deinit()
    # kit.deinit()
    print("Servos deinitialized.")

import pigpio

# Create a PWM object for the servo motor.
pwm = pigpio.PWM()

# Set the frequency of the PWM signal.
pwm.set_frequency(50)

# Set the duty cycle of the PWM signal.
pwm.set_duty_cycle(50)

# Start the PWM signal.
pwm.start(0)

# Wait for 1 second.
time.sleep(1)

# Stop the PWM signal.
pwm.stop(0)
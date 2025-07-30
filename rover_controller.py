import RPi.GPIO as GPIO
from evdev import InputDevice, categorize, ecodes
import time

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)

# Motor GPIO Setup
GPIO.setup(32, GPIO.OUT)  # 32 orange , right motor forwards
GPIO.setup(29, GPIO.OUT)  # 29 green , right motor backwards
GPIO.setup(31, GPIO.OUT)  # 31 yellow , left motor forwards
GPIO.setup(33, GPIO.OUT)  # 33 brown , left motor backwards

time.sleep(20)
# Creates object 'gamepad' to store the data
gamepad = InputDevice('/dev/input/event4')

# Button code variables (change to suit your device)
circleBtn = 305
crossBtn = 304
squareBtn = 308
triangleBtn = 307

# Prints out device info at start
print(gamepad)

# Loop to read gamepad inputs and control motors
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:  # Button pressed
            if event.code == triangleBtn:  # Triangle = up
                print("Moving Up")
                GPIO.output(32, True)  # Right motor forwards
                GPIO.output(31, True)  # Left motor forwards
            elif event.code == squareBtn:  # Square = left
                print("Moving left")
                GPIO.output(32, True)  # Right motor forwards
                GPIO.output(31, False)  # Stop left motor
                GPIO.output(33, False)  # Stop left motor
            elif event.code == circleBtn:  # Circle = right
                print("Moving right")
                GPIO.output(29, False)  # Stop right motor
                GPIO.output(31, True)  # Left motor forwards
                GPIO.output(32, False)  # Stop right motor
            elif event.code == crossBtn:  # X = down
                print("Moving Down")
                GPIO.output(29, True)  # Right motor backwards
                GPIO.output(33, True)  # Left motor backwards
                GPIO.output(32, False)  # Stop right motor forwards
                GPIO.output(31, False)  # Stop left motor forwards
        elif event.value == 0:  # Button released
            if event.code in [triangleBtn, squareBtn, circleBtn, crossBtn]:
                print("Stopping Motors")
                # Stop all motors when button is released
                GPIO.output(32, False)
                GPIO.output(29, False)
                GPIO.output(31, False)
                GPIO.output(33, False)

# Cleanup GPIO (this will run when you stop the script or press CTRL+C)
GPIO.cleanup()

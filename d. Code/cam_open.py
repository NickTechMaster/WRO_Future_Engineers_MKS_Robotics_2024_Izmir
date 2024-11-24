# Import necessary libraries
import RPi.GPIO as GPIO
import time
from gpiozero import Button, LED
import board
import adafruit_tcs34725

# Initialize the TCS34725 color sensor
i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

# Configure GPIO settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for LED control
GPIO.setup(6, GPIO.OUT)  # Unused in this script but can be configured later
GPIO.setup(11, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)

# Set initial LED states
GPIO.output(5, GPIO.HIGH)  # Set pin 5 high initially
GPIO.output(11, GPIO.LOW)  # Set pin 11 low initially
GPIO.output(9, GPIO.LOW)   # Set pin 9 low initially

# Initialize an indicator LED
led = LED(12)
led.on()

# Main loop
while True:
    try:
        # Read RGB color values from the sensor
        color_rgb = sensor.color_rgb_bytes

        # Check if the detected color falls in the range for orange
        if color_rgb[0] > 40 and color_rgb[2] < 25:
            print("orange")
            GPIO.output(9, GPIO.HIGH)  # Activate pin 9 if orange is detected
            time.sleep(1)
        else:
            GPIO.output(9, GPIO.LOW)  # Deactivate pin 9 otherwise
    except:
        # Ignore any errors and continue
        pass

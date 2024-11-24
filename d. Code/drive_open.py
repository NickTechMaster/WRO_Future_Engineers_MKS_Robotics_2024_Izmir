import RPi.GPIO as GPIO   
import time
from gpiozero import Button, LED
from mpu6050 import mpu6050

# Initialize the MPU6050 sensor
sensor = mpu6050(0x68)

# Setup initial state variables
mittelpunkt = 0

# Disable GPIO warnings
GPIO.setwarnings(False)

# Set GPIO pin numbering to BCM
GPIO.setmode(GPIO.BCM)

# Motor control pins
in1 = 24
in2 = 23
en = 25
temp1 = 1

# Setup motor control pins as output
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)

# Initialize motor pins to stop the motor
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)

# Setup PWM for motor speed control
p = GPIO.PWM(en, 1000)
p.start(0)

# Setup servo control pin
servoPIN = 17
GPIO.setup(servoPIN, GPIO.OUT)
p_s = GPIO.PWM(servoPIN, 333)

# Setup additional GPIO pins for ultrasonic sensors and button
GPIO.setup(7, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.IN)

GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.IN)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.IN)

GPIO.setup(9, GPIO.IN)

# Setup additional ultrasonic sensor pins
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.IN)

# Function to trigger ultrasonic sensor and measure distance
def ultraschall(mode):
    global distanz
    countdown = 500000

    # Set ultrasonic sensor trigger and echo pins based on mode
    if mode == 0:
        GPIO_TRIGGER = 21
        GPIO_ECHO = 20
    elif mode == 1:
        GPIO_TRIGGER = 26
        GPIO_ECHO = 19
    else:
        GPIO_TRIGGER = 27
        GPIO_ECHO = 22

    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Measure time between trigger and echo signal
    StartZeit = time.time()
    StopZeit = time.time()

    countdown = 300000

    # Wait for the echo signal to start
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()
        countdown -= 1
        if countdown <= 0:
            print("Error in sensor")
            return 1200

    # Wait for the echo signal to stop
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()
        countdown -= 1
        if countdown <= 0:
            print("Error in sensor")
            return 1200

    # Calculate distance based on time difference
    TimeElapsed = StopZeit - StartZeit
    distanz = (TimeElapsed * 34300) / 2

    return round(distanz)

# Setup initial motor direction
GPIO.output(in1, GPIO.HIGH)
GPIO.output(in2, GPIO.LOW)

# Initialize sensor data
data_90 = 0
data_270 = 0

# Initialize button and LED
button = Button(8)
led = LED(12)
led.on()

# Wait for the button to be pressed to start the servo
while True:
    if button.is_pressed:
        p_s.start(60)
        print("Start")
        break

# Set initial servo duty cycle
p_s.ChangeDutyCycle(60)

# Initialize counters for curve and no-movement detection
curves = 0
countdown = 2
countdown_2 = 1
delay_vorne = 1

no_acceleration = 0
no_acceleration_long = 0
no_acceleration_counter_long = 0

# Main loop for handling movement logic
while True:
    # Read accelerometer data
    accelerometer_data = sensor.get_accel_data()
    accelerometer_data1 = accelerometer_data["x"] * (-1)
    time.sleep(0.1)
    accelerometer_data = sensor.get_accel_data()
    accelerometer_data2 = accelerometer_data["x"] * (-1)

    # Calculate acceleration difference
    accelerometer_data = abs(accelerometer_data1 - accelerometer_data2) / 0.1

    if accelerometer_data < 3:
        no_acceleration += 1
    else:
        no_acceleration = 0

    if accelerometer_data >= 3:
        no_acceleration_long = 0

    # Detect prolonged inactivity
    if no_acceleration >= 10:
        print("No movement detected")
        p_s.ChangeDutyCycle(60)
        time.sleep(2)
        no_acceleration = 0
        no_acceleration_long += 1

    # If no movement for a long time, change motor behavior
    if no_acceleration_long >= 2:
        print("No movement for long")
        p.ChangeDutyCycle(27)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        p_s.ChangeDutyCycle(60)
        time.sleep(2)
        print("Danger detected")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        no_acceleration_long = 0
        no_acceleration_counter_long = 0

    # Track the number of curves and stop when finished
    if curves >= 12:
        countdown_2 -= 1
        print(f"End in {countdown_2} seconds")

    countdown -= 1
    if GPIO.input(9) == GPIO.HIGH and countdown <= 0:
        curves += 1
        print(f"Curve {curves}")
        countdown = 25
        if curves == 12:
            countdown_2 = 15
    if curves == 12 and countdown_2 <= 0:
        p.ChangeDutyCycle(0)
        p_s.stop()

    # Set steering control variables
    var_delay = 0
    var_lenkung_r = 0.15
    var_lenkung_l = 0.15
    g = 10

    # Measure distance for 90 and 270 degree angles
    value = ultraschall(1)
    if value < 1000:
        data_90 = value
        print(f"Data 90: {data_90}")
    else:
        print("Error: value too high")

    value = ultraschall(0)
    if value < 1000:
        data_270 = value
        print(f"Data 270: {data_270}")
    else:
        print("Error: value too high")

    # Adjust steering based on distance data
    if data_270 != 0 and data_90 != 0 and data_270 < 5500 and data_90 < 5500:
        calc = round((((((100 - ((100 * data_90) / (((data_270 + data_90) / 2)))) / 10)) ** 7) / g)

        # Limit steering adjustment
        if calc > 5:
            if calc > 100 or calc < -100:
                calc = 100
            p_s.ChangeDutyCycle(60 + abs(calc) * var_lenkung_r)
            time.sleep(0.001)
        elif calc < -15:
            if calc > 100 or calc < -100:
                calc = -100
            p_s.ChangeDutyCycle(60 - abs(calc) * var_lenkung_l)
            time.sleep(0.001)
        else:
            p_s.ChangeDutyCycle(60)

    # Update motor speed
    p.ChangeDutyCycle(35)

    # Small delay 
    time.sleep(var_delay)

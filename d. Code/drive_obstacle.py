# Import necessary libraries
import RPi.GPIO as GPIO   
import time
from gpiozero import Button, LED
import board
import busio
import adafruit_vl53l0x
from mpu6050 import mpu6050

# Initializing constants and variables
servo_cam_mitte = 70  # Initial servo position for camera
sensor = mpu6050(0x68)  # Initialize MPU6050 sensor for accelerometer
mittelpunkt = 0  # Variable to store midpoint value
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering to BCM

# Setup motor control pins
in1, in2, en = 24, 23, 25
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)  # PWM control for motor speed
p.start(0)  # Start PWM with 0% duty cycle (motor off)

# Setup servo control pins
servoPIN = 17
GPIO.setup(servoPIN, GPIO.OUT)
p_s = GPIO.PWM(servoPIN, 333)  # PWM for steering servo

servoPIN_cam = 18
GPIO.setup(servoPIN_cam, GPIO.OUT)
p_s_c = GPIO.PWM(servoPIN_cam, 333)  # PWM for camera servo

# Setup other GPIO pins for ultrasonic sensors and button inputs
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.IN)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.IN)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.IN)
GPIO.setup(6, GPIO.IN)
GPIO.setup(4, GPIO.IN)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)  # Initialize output pin 13 to LOW
GPIO.setup(9, GPIO.IN)
GPIO.setup(5, GPIO.IN)

# Ultrasonic function to calculate distance
def ultraschall(mode):
    global distanz
    countdown = 50000

    # Select pins based on mode (0, 1, 2)
    if mode == 0:
        GPIO_TRIGGER, GPIO_ECHO = 21, 20
    elif mode == 1:
        GPIO_TRIGGER, GPIO_ECHO = 26, 19
    else:
        GPIO_TRIGGER, GPIO_ECHO = 27, 22

    # Trigger ultrasonic sensor
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartZeit = time.time()
    StopZeit = time.time()

    # Wait for echo response and measure duration
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()
        countdown -= 1
        if countdown <= 0:
            print(f"Ultrasonic error in mode {mode}")
            return 1200

    countdown = 7000
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()
        countdown -= 1
        if countdown <= 0:
            print(f"Ultrasonic error in mode {mode}")
            return 1200

    # Calculate distance
    TimeElapsed = StopZeit - StartZeit
    distanz = (TimeElapsed * 34300) / 2
    return round(distanz)

# Initialize LEDs
led = LED(12)
led.on()

# Initialize button
button = Button(8)

# Wait for button press to start
while True:
    if button.is_pressed:
        p_s.start(60)
        p_s_c.start(servo_cam_mitte)
        print("Button pressed, starting motors and servos.")
        break
    else:
        pass

# Initialize control variables
countdown_2 = 25
forward = 0
red_stone, green_stone, purple_stone = 0, 0, 0
delay_vorne = 1
counter_sides, counter_after_curve = 10, 0
right, left = False, False
no_acceleration, no_acceleration_long, no_acceleration_counter_long = 0, 0, 0
countdown_cam = 0

# Main loop
while True:
    # Camera servo control based on countdown
    if countdown_cam < 3:
        p_s_c.ChangeDutyCycle(servo_cam_mitte)
    elif countdown_cam < 4:
        p_s_c.ChangeDutyCycle(servo_cam_mitte + 17)
    elif countdown_cam < 5:
        p_s_c.ChangeDutyCycle(servo_cam_mitte)
    elif countdown_cam < 6:
        p_s_c.ChangeDutyCycle(servo_cam_mitte - 17)
    else:
        countdown_cam = 0
    countdown_cam += 1

    # Read accelerometer data and detect movement
    accelerometer_data1 = sensor.get_accel_data()["x"] * (-1)
    time.sleep(0.1)
    accelerometer_data2 = sensor.get_accel_data()["x"] * (-1)
    accelerometer_data = abs(accelerometer_data1 - accelerometer_data2) / 0.1

    # If no significant acceleration, trigger motion detection
    if accelerometer_data < 3:
        no_acceleration += 1
    else:
        no_acceleration = 0

    # Handle case of long-term lack of acceleration
    if no_acceleration >= 10:
        print("No movement detected for a while.")
        p.ChangeDutyCycle(30)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        p_s.ChangeDutyCycle(60)
        time.sleep(2)
        print("Warning: danger detected, moving back.")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        no_acceleration_long += 1

    if no_acceleration_long >= 2:
        print("No movement detected for a long time.")
        p.ChangeDutyCycle(30)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        p_s.ChangeDutyCycle(60)
        time.sleep(2)
        print("Warning: danger detected, moving back.")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        no_acceleration_long = 0

    # Handle ultrasonic sensor readings and object detection
    vorne = ultraschall(3)
    if vorne > 1000:
        print("Error: ultrasonic sensor 3 returned too high value.")
        vorne = 50

    value_90 = ultraschall(1)
    if value_90 < 1000:
        if value_90 < 5.5:
            p.ChangeDutyCycle(30)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            p_s.ChangeDutyCycle(60)
            time.sleep(1)
            print("Warning: danger detected in front (90 degrees).")
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
        data_90 = value_90
    else:
        print("Error: ultrasonic sensor 1 returned too high value.")

    # Repeat for another ultrasonic sensor (270 degrees)
    value_270 = ultraschall(0)
    if value_270 < 1000:
        data_270 = value_270
        if value_270 < 5.5:
            p.ChangeDutyCycle(30)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            p_s.ChangeDutyCycle(60)
            time.sleep(1)
            print("Warning: danger detected in front (270 degrees).")
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
    else:
        print("Error: ultrasonic sensor 0 returned too high value.")

    # Handle steering logic based on ultrasonic data
    if data_270 != 0 and data_90 != 0 and data_270 < 5500 and data_90 < 5500:
        mittelpunkt = (data_270 + data_90) / 2  # Calculate the midpoint between sensors

        # Adjust the steering based on sensor readings
        if mittelpunkt < 100:
            GPIO.output(13, GPIO.HIGH)
        else:
            GPIO.output(13, GPIO.LOW)

        # If the robot is near an obstacle, adjust direction accordingly
        if mittelpunkt > 280 and counter_sides <= 0 and vorne < 50:
            p.ChangeDutyCycle(30)
            p_s.ChangeDutyCycle(60)
            x = 0
            while x < 12:
                time.sleep(0.1)
                vorne = ultraschall(3)
                if vorne > 1000:
                    print("Error: value too high for front sensor")
                    vorne = 50
                if vorne < 20:  # If the front is blocked, take action to avoid it
                    if delay_vorne == 1:
                        delay_vorne = 0
                    else:
                        p.ChangeDutyCycle(30)
                        GPIO.output(in1, GPIO.LOW)
                        GPIO.output(in2, GPIO.HIGH)
                        p_s.ChangeDutyCycle(60)
                        time.sleep(0.5)
                        print("Danger ahead!")
                        GPIO.output(in1, GPIO.HIGH)
                        GPIO.output(in2, GPIO.LOW)
                x += 1
            # Adjust steering based on sensor readings
            if data_90 > data_270:
                p_s.ChangeDutyCycle(69)
                right = True
            else:
                p_s.ChangeDutyCycle(53)
                left = True
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            time.sleep(2)
            p_s.ChangeDutyCycle(60)
            time.sleep(0.2)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            counter_sides = 22
            counter_after_curve = 10
        else:
            counter_sides -= 1  # Decrease the side counter if no obstacle is detected

    # Adjust steering based on distance readings
    if data_270 <= data_90:
        lenkung = round(100 - (100 * data_270 / mittelpunkt))
        if lenkung > 5:
            einlenkung = round(60 - lenkung * var_lenkung_r)
            if einlenkung >= 20:
                p_s.ChangeDutyCycle(einlenkung - 3)
            else:
                p_s.ChangeDutyCycle(53)
        else:
            p_s.ChangeDutyCycle(60)

    elif data_90 <= data_270:
        lenkung = round(100 - (100 * data_90 / mittelpunkt))
        if lenkung > 5:
            einlenkung = round(60 + lenkung * var_lenkung_l)
            if einlenkung <= 50:
                p_s.ChangeDutyCycle(einlenkung + 3)
            else:
                p_s.ChangeDutyCycle(69)
        else:
            p_s.ChangeDutyCycle(60)

    # Handle red stone detection
    if GPIO.input(6) == GPIO.HIGH:
        red_stone += 1
    else:
        red_stone = 0

    # Handle green stone detection
    if GPIO.input(4) == GPIO.HIGH:
        green_stone += 1
    else:
        green_stone = 0

    # Handle purple stone detection
    if GPIO.input(5) == GPIO.HIGH:
        purple_stone += 1
    else:
        purple_stone = 0

    # Handle purple stone color handling
    if purple_stone > 1:  # Check if there are more than 1 purple stones detected
        red_stone = 0  # Reset red stone count
        green_stone = 0  # Reset green stone count
        vanished_purple = 0  # Initialize counter for vanished purple stones
    
        while vanished_purple < 6:  # Keep looking for purple stones until 6 vanish
            vorne = ultraschall(3)  # Get distance from front ultrasonic sensor (sensor 3)
            print(str(vanished_purple) + " purple")  # Print the current count of vanished purple stones
    
            if GPIO.input(5) == GPIO.LOW:  # If the sensor detects a change (stone lost)
                vanished_purple += 1  # Increment the vanished counter
    
            if vorne < 35:  # If an obstacle is too close (less than 35 cm)
                p.ChangeDutyCycle(30)  # Slow down the motor
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)  # Reverse the robot
                p_s.ChangeDutyCycle(60)  # Adjust the servo speed
    
                time.sleep(1)  # Wait for 1 second
                print("gefahr_purple")  # Danger message for purple stone
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)  # Move forward again
                p.ChangeDutyCycle(tempo_stein)  # Set motor speed back to normal
    
            # Left side sensor (1)
            value = ultraschall(1)
            if value < 1000:  # If a valid sensor reading is obtained
                if value < 8:  # If obstacle is too close (less than 8 cm)
                    p.ChangeDutyCycle(30)
                    GPIO.output(in1, GPIO.LOW)
                    GPIO.output(in2, GPIO.HIGH)  # Reverse
                    p_s.ChangeDutyCycle(60)
                    time.sleep(1)  # Wait
                    print("gefahr_ultraschall")  # Danger message for left sensor
                    GPIO.output(in1, GPIO.HIGH)
                    GPIO.output(in2, GPIO.LOW)  # Move forward again
                data_90 = value  # Store the distance data
    
            time.sleep(0.05)  # Short delay
    
            # Right side sensor (0)
            value = ultraschall(0)
            if value < 1000:  # If a valid sensor reading is obtained
                data_270 = value  # Store the distance data
                if value < 8:  # If obstacle is too close
                    p.ChangeDutyCycle(30)
                    GPIO.output(in1, GPIO.LOW)
                    GPIO.output(in2, GPIO.HIGH)  # Reverse
                    p_s.ChangeDutyCycle(60)
                    time.sleep(1)  # Wait
                    print("gefahr_ultraschall")  # Danger message for right sensor
                    GPIO.output(in1, GPIO.HIGH)
                    GPIO.output(in2, GPIO.LOW)  # Move forward again
    
            # Steering adjustment for turning based on sensor data
            if data_270 <= data_90:
                lenkung = round(100 - (100 * data_270 / mittelpunkt))  # Calculate steering angle
                if lenkung > 5:
                    einlenkung = round(60 - lenkung * var_lenkung_r)  # Adjust steering for right turns
                    if einlenkung >= 20:
                        p_s.ChangeDutyCycle(einlenkung - 3)  # Apply steering adjustment
                    else:
                        p_s.ChangeDutyCycle(53)  # Neutral steering
                else:
                    p_s.ChangeDutyCycle(60)  # Straight steering
    
            # Steering adjustment for left turns
            elif data_90 <= data_270:
                lenkung = round(100 - (100 * data_90 / mittelpunkt))  # Calculate steering angle
                if lenkung > 5:
                    einlenkung = round(60 + lenkung * var_lenkung_l)  # Adjust steering for left turns
                    if einlenkung <= 50:
                        p_s.ChangeDutyCycle(einlenkung + 3)  # Apply steering adjustment
                    else:
                        p_s.ChangeDutyCycle(70)  # Stronger turn
                else:
                    p_s.ChangeDutyCycle(60)  # Neutral steering

    # Handle red stone color handling
    if red_stone >= 1:  # Check if a red stone is detected
        counter_red = 0  # Initialize counter for red stone detection
        vanished = 0  # Initialize counter for missing red stones
        print("____________________________")
        print("red")  # Print message for red stone detection
        time.sleep(0.05)
    
        p.ChangeDutyCycle(tempo_stein)  # Set motor speed for red stone handling
    
        while ultraschall(1) > 14:  # Continue if the front distance is greater than 14 cm
            if GPIO.input(9) == GPIO.HIGH:  # If the stop button is pressed, break the loop
                print("break color")
                break
            time.sleep(0.05)
            vorne = ultraschall(3)  # Get distance from front sensor
            time.sleep(0.05)
    
            if GPIO.input(6) != GPIO.HIGH:  # If sensor 6 is not active, increment vanished count
                vanished += 1
    
            p_s.ChangeDutyCycle(50)  # Adjust servo speed
            counter_red += 1  # Increment red stone counter
    
            if vorne < 35:  # If an obstacle is too close (less than 35 cm)
                p.ChangeDutyCycle(30)
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)  # Reverse
                p_s.ChangeDutyCycle(60)
                time.sleep(1)  # Wait
                print("gefahr_red")  # Danger message for red stone
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)  # Move forward again
                p.ChangeDutyCycle(tempo_stein)
    
            print(f"counter red: {counter_red}    vanished: {vanished}")  # Debug output
    
            if counter_red > 35:  # If red stone counter exceeds threshold, adjust servo
                print(counter_red)
                p_s.ChangeDutyCycle(68)  # Adjust servo speed
                time.sleep(0.5)  # Wait
                counter_red = 0  # Reset red stone counter
    
            if vanished > 3:  # If more than 3 vanished red stones, stop the loop
                print("abgebrochen")  # Break message
                p_s.ChangeDutyCycle(68)  # Adjust servo speed
                time.sleep(0.5)  # Wait
                vanished = 0  # Reset vanished counter
                break  # Exit loop
    
        print("ende")  # End of red stone processing
        print("____________________________")
        
    else:
        counter_red = 0 # Reset counter
        p.ChangeDutyCycle(tempo) # Change motor speed

    # Handle green stone color handling   
    if green_stone >= 1:  # Check if a green stone is detected
        counter_red = 0  # Reset red stone counter
        vanished = 0  # Reset vanished counter
        print("____________________________")
        print("green")  # Print message for green stone detection
        time.sleep(0.05)
    
        p.ChangeDutyCycle(tempo_stein)  # Set motor speed for green stone handling
    
        while ultraschall(0) > 18:  # Continue if the right distance is greater than 18 cm
            if GPIO.input(9) == GPIO.HIGH:  # If stop button is pressed, break the loop
                print("break color")
                break
            time.sleep(0.05)
            vorne = ultraschall(3)  # Get distance from front sensor
            time.sleep(0.05)
    
            if GPIO.input(4) != GPIO.HIGH:  # If sensor 4 is not active, increment vanished count
                vanished += 1
    
            p_s.ChangeDutyCycle(69)  # Adjust servo speed for green stone
            counter_red += 1  # Increment green stone counter
    
            if vorne < 30:  # If obstacle is too close (less than 30 cm)
                p.ChangeDutyCycle(30)
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)  # Reverse
                p_s.ChangeDutyCycle(60)
                time.sleep(1)  # Wait
                print("gefahr_green")  # Danger message for green stone
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)  # Move forward again
    
            print(f"counter green: {counter_red}    vanished: {vanished}")  # Debug output
    
            if counter_red > 15:  # If green stone counter exceeds threshold, adjust servo
                print(counter_red)
                p_s.ChangeDutyCycle(55)  # Adjust servo speed
                time.sleep(0.5)  # Wait
                counter_red = 0  # Reset green stone counter
    
            if vanished > 3:  # If more than 3 vanished green stones, stop the loop
                print("abgebrochen")  # Break message
                p_s.ChangeDutyCycle(55)  # Adjust servo speed
                time.sleep(0.5)  # Wait
                vanished = 0  # Reset vanished counter
                break  # Exit loop
    
        print("ende")  # End of green stone processing
        print("____________________________")
    
        p_s.ChangeDutyCycle(57)  # Reset servo speed
        
    else:
        counter_red = 0 # Reset counter
        p.ChangeDutyCycle(tempo) # Change motor speed

    var_delay = 0.05  # Short delay between actions
    
    if vorne < 13:  # If an obstacle is detected too close in front
        if delay_vorne == 1:  # If there is a delay, reverse the flag
            delay_vorne = 0
        else:
            p.ChangeDutyCycle(30)  # Slow down
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)  # Reverse
            p_s.ChangeDutyCycle(60)
            time.sleep(1.3)  # Wait
            print("gefahr")  # Danger message
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)  # Move forward again
    
    p.ChangeDutyCycle(tempo)  # Set motor speed back to normal
    
    time.sleep(var_delay)  # Short delay before the next iteration

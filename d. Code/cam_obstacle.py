# Import necessary libraries
import RPi.GPIO as GPIO
import time
import cv2
from gpiozero import Button, LED
import numpy as np
import serial
import board
import adafruit_tcs34725

# Initialize video capture
cap = cv2.VideoCapture(-1)
time.sleep(3)

# Counters for detecting color occurrences
zähler_r = 0
zähler = 0
zähler_p = 0

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for LED control
GPIO.setup(6, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

# Turn off all LEDs initially
GPIO.output(5, GPIO.LOW)
GPIO.output(11, GPIO.LOW)
GPIO.output(9, GPIO.LOW)
GPIO.output(14, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(4, GPIO.LOW)
GPIO.output(6, GPIO.LOW)

# Initialize an LED to signal readiness
led = LED(12)
led.on()

# Variables for tracking detected colors and curves
first = " "
curves = 0
countdown_curves = 0

# Main loop
while True:
    try:
        # Capture frame and convert to HSV color space
        ret, image = cap.read()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define HSV range for green detection
        g_hmin, g_smin, g_vmin = 45, 71, 26
        g_hmax, g_smax, g_vmax = 75, 205, 99
        lower_green = np.array([g_hmin, g_smin, g_vmin])
        upper_green = np.array([g_hmax, g_smax, g_vmax])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        # Define HSV range for red detection
        r_hmin, r_smin, r_vmin = 175, 155, 79
        r_hmax, r_smax, r_vmax = 179, 255, 194
        lower_red = np.array([r_hmin, r_smin, r_vmin])
        upper_red = np.array([r_hmax, r_smax, r_vmax])
        mask_red = cv2.inRange(hsv, lower_red, upper_red)

        # Define HSV range for purple detection (placeholder values)
        p_hmin, p_smin, p_vmin = 0, 0, 0
        p_hmax, p_smax, p_vmax = 0, 0, 0
        lower_purple = np.array([p_hmin, p_smin, p_vmin])
        upper_purple = np.array([p_hmax, p_smax, p_vmax])
        mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)

        # Flags to indicate if a color is detected
        green = False
        red = False
        purple = False
        h_g = h_r = h_p = 0

        # Process contours for green detection
        contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if 1000 < area < 110000:
                x, y, w, h = cv2.boundingRect(contour)
                if (h / w) < 3 and h > 50 and w < 200:
                    zähler += 1
                    if zähler >= 5:
                        green = True
                        h_g = h
                else:
                    zähler = 0

        # Process contours for red detection
        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if 1000 < area < 1100000:
                x, y, w, h = cv2.boundingRect(contour)
                if (h / w) < 3 and h > 60 and w < 300:
                    zähler_r += 1
                    if zähler_r >= 2:
                        red = True
                        h_r = h
                else:
                    zähler_r = 0

        # Process contours for purple detection
        contours, _ = cv2.findContours(mask_purple, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if 1000 < area < 11000000:
                x, y, w, h = cv2.boundingRect(contour)
                zähler_p += 1
                if zähler_p >= 2:
                    purple = True
                    h_p = h

        # Control GPIO based on detected colors and their relative sizes
        if green and red:
            if h_g > h_r:
                print("green_p")
                GPIO.output(4, GPIO.HIGH)
                GPIO.output(6, GPIO.LOW)
                GPIO.output(5, GPIO.LOW)
            else:
                print("red_p")
                GPIO.output(6, GPIO.HIGH)
                GPIO.output(4, GPIO.LOW)
                GPIO.output(5, GPIO.LOW)

        elif green and purple:
            if h_g > h_p:
                print("green_p")
                GPIO.output(4, GPIO.HIGH)
                GPIO.output(6, GPIO.LOW)
                GPIO.output(5, GPIO.LOW)
            else:
                print("purple_p")
                GPIO.output(5, GPIO.HIGH)
                GPIO.output(6, GPIO.LOW)
                GPIO.output(4, GPIO.LOW)

        elif red and purple:
            print("purple_p")
            GPIO.output(5, GPIO.HIGH)
            GPIO.output(6, GPIO.LOW)
            GPIO.output(4, GPIO.LOW)

        elif green:
            print("green")
            GPIO.output(4, GPIO.HIGH)
            GPIO.output(6, GPIO.LOW)
            GPIO.output(5, GPIO.LOW)

        elif red:
            print("red")
            GPIO.output(6, GPIO.HIGH)
            GPIO.output(4, GPIO.LOW)
            GPIO.output(5, GPIO.LOW)

        elif purple:
            print("purple")
            GPIO.output(5, GPIO.HIGH)
            GPIO.output(6, GPIO.LOW)
            GPIO.output(4, GPIO.LOW)

        else:
            GPIO.output(6, GPIO.LOW)
            GPIO.output(4, GPIO.LOW)
            GPIO.output(5, GPIO.LOW)

    except:
        print("error")

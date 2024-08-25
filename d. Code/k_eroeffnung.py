#importieren der bibiliotheken
import RPi.GPIO as GPIO   
import time
from gpiozero import Button, LED
import board
import adafruit_tcs34725


#anstuerrung des Farbsensors
i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)


#)

#Einstellung der übertragungs GPIO pins
GPIO.setwarnings(False)


GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5,GPIO.HIGH)
GPIO.output(11,GPIO.LOW)
GPIO.output(9,GPIO.LOW)

#ansteuerrung der LED
led = LED(12) 
led.on()

#Endlosschleife
while True:

    #überprüfen ob orangene Farbe erkannt wird wenn ja signal senden
    color_rgb = sensor.color_rgb_bytes
    if color_rgb[0] > 35 and color_rgb[2] < 13:
        print("orange")
        GPIO.output(9,GPIO.HIGH)
    else:
        GPIO.output(9,GPIO.LOW)




  

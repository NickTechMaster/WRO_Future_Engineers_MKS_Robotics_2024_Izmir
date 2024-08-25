#importieren der bibiliotheken
import RPi.GPIO as GPIO   
import time
import cv2
from gpiozero import Button, LED
import numpy as np
import board
import adafruit_tcs34725


#Ansteuerung des Farbsensors
i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)




#Ansteuerrung der Kamera
cap = cv2.VideoCapture(0)
time.sleep(3)

#definieren von Variablen
zähler_r = 0
zähler = 0
first = " "

#Konfiguration der GPIO-Pins
GPIO.setwarnings(False)


GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5,GPIO.HIGH)
GPIO.output(11,GPIO.LOW)
GPIO.output(9,GPIO.LOW)
GPIO.output(14,GPIO.LOW)

#Ansteuerrung der LED
led = LED(12) 
led.on()


while True:
    #Farbsensor Werte abfragen und bei erkennung Signal senden
    color_rgb = sensor.color_rgb_bytes
    if color_rgb[0] > 35 and color_rgb[2] < 13:
        if first == " " or first == "o":
            print("orange")
            first = "o"
            GPIO.output(14,GPIO.LOW)
            GPIO.output(9,GPIO.HIGH)
    elif color_rgb[2] > 6.2 and color_rgb[0] > 24.6 and color_rgb[1] > 24.6:
        if first == " " or first == "b":
            print("blue")
            first = "b"
            GPIO.output(9,GPIO.LOW)
            GPIO.output(14,GPIO.HIGH)
    else:
        GPIO.output(9,GPIO.LOW)
        GPIO.output(14,GPIO.LOW)

    #Bild abfragen und zu HSV Farbraum konvertieren
    ret, image = cap.read()

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #definieren von Farbwerten und erstellung von Masken
    g_hmin = g_smin = g_vmin = g_hmax = g_hmax = g_hmax = 0
    g_hmin = 36
    g_smin = 50
    g_vmin = 39
    g_hmax = 87
    g_smax = 138
    g_vmax = 172

    lower = np.array([g_hmin, g_smin, g_vmin])
    upper = np.array([g_hmax, g_smax, g_vmax])
    mask_green = cv2.inRange(hsv, lower, upper)



    r_hmin = r_smin = r_vmin = r_hmax = r_hmax = r_hmax = 0
    r_hmin = 116
    r_smin = 164
    r_vmin = 140
    r_hmax = 179
    r_smax = 221
    r_vmax = 224

    lower = np.array([r_hmin, r_smin, r_vmin])
    upper = np.array([r_hmax, r_smax, r_vmax])
    mask_red = cv2.inRange(hsv, lower, upper)

    #definieren von Variablen
    green = False
    red = False
    h_g = 0
    h_r = 0

    #erkennen von Kontouren der grünen Maske
    contours, hierarchy = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



    #Zeichne Rechtecke um die Konturen, die den grünen Kriterien entsprechen
    for contour in contours:
        area = cv2.contourArea(contour)
        #area = 10
        if area > 1000 and area < 110000: # nur Konturen berücksichtigen, die größer als eine bestimmte Fläche sind
            
            (x, y, w, h) = cv2.boundingRect(contour)
            if (h / w) < 3: # nur Konturen berücksichtigen, die ein Längen-Breiten-Verhältnis von weniger als 3 haben
                if h > 50 and w < 200:
                    zähler = zähler + 1
                    if zähler >= 5:
                        green = True
                        h_g = h
                        

                else:
                    zähler = 0




    #erkennen von Kontouren der roten Maske
    contours, hierarchy = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Zeichne Rechtecke um die Konturen, die den grünen Kriterien entsprechen
    for contour in contours:
        area = cv2.contourArea(contour)
        #area = 10
        if area > 1000 and area < 1100000: # nur Konturen berücksichtigen, die größer als eine bestimmte Fläche sind
            
            (x, y, w, h) = cv2.boundingRect(contour)
            if (h / w) < 3: # nur Konturen berücksichtigen, die ein Längen-Breiten-Verhältnis von weniger als 3 haben
                if h > 60 and w < 300:
                    zähler_r = zähler_r + 1
                    if zähler_r >= 2:
                        #cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        #print("red")
                        red = True
                        h_r = h
                        
                else:
                    zähler_r = 0



    #senden von signalen je nach Ergebnissen
    if green == True and red == True:
        if h_g > h_r:
            print("green_p")
            GPIO.output(6,GPIO.HIGH)
            GPIO.output(5,GPIO.LOW)
        else:
            print("red_p")
            GPIO.output(11,GPIO.HIGH)
            GPIO.output(6,GPIO.LOW)
    elif green == True:
        print("green")
        GPIO.output(6,GPIO.HIGH)
        GPIO.output(11,GPIO.LOW)
    elif red == True:
        print("red")
        GPIO.output(11,GPIO.HIGH)
        GPIO.output(6,GPIO.LOW)
       
    else:
        GPIO.output(6,GPIO.LOW)
        GPIO.output(11,GPIO.LOW)



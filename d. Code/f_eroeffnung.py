#importieren der bibiliotheken
import RPi.GPIO as GPIO   
import time
import cv2
from gpiozero import Button, LED


#definieren variablen
switch = 0

counter = 0

counter_2 = 0

mittelpunkt = 0

switch_2 = 5

data_90 = 0

data_270 = 0
#GPIO einstellungen und configuration
GPIO.setwarnings(False)


GPIO.setmode(GPIO.BCM)

#gpio configurationen von dem Motor
in1 = 24
in2 = 23
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)

p.start(0)

GPIO.setup(13, GPIO.IN)

#gpio configurationen von dem servo motor
servoPIN = 17
GPIO.setup(servoPIN, GPIO.OUT)
p_s = GPIO.PWM(servoPIN, 50)




#gpio configurationen von den ultraschall sensoren
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.IN)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.IN)

GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.IN)


#funktion um ultraschall werte zu verarbeiten, und abstand zu errechnen
def ultraschall(mode):
    global distanz
    countdown = 100

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

    StartZeit = time.time()
    StopZeit = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()
        countdown = countdown - 1
        if countdown <= 0:
            print("fehler")
            return(1200)

    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()

    TimeElapsed = StopZeit - StartZeit
    distanz = (TimeElapsed * 34300) / 2

    return(round(distanz))

#control pins damit ich dem motor sagen kann ob er vorwärts oder rückwärts fahren soll
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)


#Ansteuerung der LED
led = LED(12) 
led.on()


#configuration der übertragungs pins zwischen den beiden Raspberrypis
GPIO.setup(5, GPIO.IN)
GPIO.setup(6, GPIO.IN)
GPIO.setup(13, GPIO.IN)


#Ansteuerung des Knopfes und warten dass er gedrückt wird
button = Button(7)
while True:
    if button.is_pressed:
        print("start")
        break
    else:
        pass

p_s.start(8)
#Endlosschleife die die gnaze Zeit ausgeführt wird
while True:
    #werte der übertragungspins abfragen
    if GPIO.input(13) == GPIO.HIGH and switch == 0 :
        counter = counter + 1
        print("Kurve: Orange" + " " + str(counter))
        switch = 18

    #definieren von variablen die für die fahrweise wichtig sind
    var_delay = 0.002

    var_lenkung_r = 0.038

    var_lenkung_l = 0.1


    #holen von dem rechten ultrschall wert
    value = ultraschall(1)
    if value < 1000:
        data_90 = value

    #holen von dem linken ultraschall wert
    value = ultraschall(0)
    if value < 1000:
        data_270 = value


#überrüfen ob werte fehler haben wenn, nein wird code fortgesetzt
    if data_270 != 0 and data_90 != 0 and data_270 < 5500 and data_90 < 5500:

        #mittelpunkt zwischen den beiden äußeren ultrachallsensoren berechnen
        mittelpunkt = (data_270 + data_90) / 2

        #berechnung der benötigten lenkung für rechts
        if data_270 <= data_90:
            lenkung = round(100 - (100 * data_270 / mittelpunkt))
            if lenkung > 18:
                einlenkung = 8-lenkung*var_lenkung_r
                if einlenkung > 5.9:
                    p_s.ChangeDutyCycle(einlenkung)
                else:
                    p_s.ChangeDutyCycle(5.9)
                    
            time.sleep(0.001)

        #berechnung der benötigten lenkung für links
        elif data_90 <= data_270:
            lenkung = round(100 - (100 * data_90 / mittelpunkt))
            if lenkung > 15:
                einlenkung = 8+lenkung*var_lenkung_l
                if einlenkung < 10.7:
                    #print(einlenkung)
                    p_s.ChangeDutyCycle(einlenkung)#
                else:
                    #print("angepasst")
                    p_s.ChangeDutyCycle(10.7)
            time.sleep(0.001)
    

    #zähler damit kurven script nicht zu oft hintereinander ausgeführt werden kann
    if data_90 < 260 and data_270 < 260 and mittelpunkt < 90:
        switch_2 = switch_2 - 1
        if switch_2 <= 0:
            if switch >= 1:
                switch = switch - 1
                switch_2 = 4
    else:
        switch_2 = 4

    #überprüfen ob 12 Kurven gefahren wurden
    if counter >= 12:
        print("Ende")

        #warten bis alle ultraschall sensoren werte haben, sodass er weiß das er im End-Bereich steht, wenn ja stoppt er
        if ultraschall(2) <= 198 and ultraschall(2) >= 150 and mittelpunkt < 80:
            counter_2 = counter_2 + 1
            if counter_2 > 12:
                p.ChangeDutyCycle(0)
                print("Ende_Ende")
                while True:
                    pass
        else:
            counter_2 = 0

    #starte motor mit Geschwindigkeit 31
    p.ChangeDutyCycle(36)

    #warte funktion, damit servo nicht sooft hintereinander lenken muss
    time.sleep(var_delay)

#importieren der bibiliotheken
import RPi.GPIO as GPIO   
import time
from gpiozero import Button, LED


#definieren von variablen
switch = 0

counter = 0

mittelpunkt = 0

switch_2 = 5

data_90 = 0

data_270 = 0

counter_green = 0

counter_red = 0

curve = " "

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

GPIO.setup(18, GPIO.OUT)
GPIO.setup(8, GPIO.IN)


#funktion um ultraschall werte zu verarbeiten, und abstand zu errechnen
def ultraschall(mode):
    global distanz
    countdown = 500

    if mode == 0:
        GPIO_TRIGGER = 21
        GPIO_ECHO = 20
        
    elif mode == 1:
        GPIO_TRIGGER = 26
        GPIO_ECHO = 19
        
    elif mode == 2:
        GPIO_TRIGGER = 27
        GPIO_ECHO = 22
    
    else:
        GPIO_TRIGGER = 18
        GPIO_ECHO = 8
      
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
GPIO.setup(15, GPIO.IN)


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
    #Erkennung ob eine orangene Kurve erkannt wurde
    if GPIO.input(13) == GPIO.HIGH and switch == 0 :
        if curve == " " or curve == "o":
            #Mannöver für die orangene Kurve
            print("Kurve: Orange")
            while ultraschall(2) > 40: 

                p.ChangeDutyCycle(tempo)
                p_s.ChangeDutyCycle(7.3)
                time.sleep(0.2)
            p.ChangeDutyCycle(0)

            p.ChangeDutyCycle(tempo + 10)
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            p_s.ChangeDutyCycle(6)
            time.sleep(1)
            while ultraschall(3) > 49:
                time.sleep(0.2)
                if ultraschall(3) < 25:
                    print("hi")
                    p.ChangeDutyCycle(tempo)
                    GPIO.output(in1,GPIO.HIGH)
                    GPIO.output(in2,GPIO.LOW)
                    time.sleep(1)
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.HIGH)
                time.sleep(0.2)
                p.ChangeDutyCycle(tempo + 10)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                p_s.ChangeDutyCycle(6)
            p.ChangeDutyCycle(tempo)
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            p_s.ChangeDutyCycle(6)
            time.sleep(0.5)

            switch = 14

    #Erkennung ob eine blaue Kurve erkannt wurde
    elif GPIO.input(15) == GPIO.HIGH:
        if curve == " " or curve == "b":
            curve = "b"
            #Mannöver für die blaue Kurve
            while ultraschall(2) > 32: 
                p.ChangeDutyCycle(tempo)
                p_s.ChangeDutyCycle(9.7)
                time.sleep(0.2)
            p.ChangeDutyCycle(0)

            p.ChangeDutyCycle(35)
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            p_s.ChangeDutyCycle(10.3)
            time.sleep(3)
            while ultraschall(3) > 49:
                time.sleep(0.2)
                p.ChangeDutyCycle(45)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                p_s.ChangeDutyCycle(10.3)
            p.ChangeDutyCycle(0)
            time.sleep(1)
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)

            switch = 14


            print("Kurve: Blau")



    #definieren von variablen die für die fahrweise wichtig sind
    var_delay = 0.002

    var_lenkung_r = 0.03

    var_lenkung_l = 0.04

    tempo = 29
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
                einlenkung = round(8-lenkung*var_lenkung_r)
                if einlenkung > 7:
                    p_s.ChangeDutyCycle(einlenkung)
                else:
                    
                    p_s.ChangeDutyCycle(7)
            time.sleep(0.001)

        #berechnung der benötigten lenkung für links
        elif data_90 <= data_270:
            lenkung = round(100 - (100 * data_90 / mittelpunkt))
            if lenkung > 15:
                einlenkung = round(8+lenkung*var_lenkung_l)
                if einlenkung < 10.7:
                    
                    p_s.ChangeDutyCycle(einlenkung)#
                else:
                    
                    p_s.ChangeDutyCycle(10.7)
            time.sleep(0.001)
    


    vorne = ultraschall(2)

    #ausweichmannöver wenn Auto zu nahe an die Bande kommt
    if vorne < 13:
        if curve == "o":
            p.ChangeDutyCycle(tempo)
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            p_s.ChangeDutyCycle(5.9)
            time.sleep(1)
            print("gefahr")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            p.ChangeDutyCycle(tempo)
        else:
            p.ChangeDutyCycle(tempo)
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            p_s.ChangeDutyCycle(5.9)
            time.sleep(1)
            print("gefahr")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            p.ChangeDutyCycle(tempo)

    #überprüfen ob übertragungspins grün sagen
    if GPIO.input(6) == GPIO.HIGH:

        #Ausweichmannöver für grüne Steine
        print("green")
        p.ChangeDutyCycle(tempo)
        counter_green = 0
        while ultraschall(1) > 21:
            if GPIO.input(13) == GPIO.HIGH:
                break
            p_s.ChangeDutyCycle(5.9)
            counter_green = counter_green + 1
            if ultraschall(2) < 30:
                p.ChangeDutyCycle(tempo)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                p_s.ChangeDutyCycle(5.9)
                time.sleep(1)
                print("gefahr_green")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                p.ChangeDutyCycle(tempo)
                p_s.ChangeDutyCycle(10)
                time.sleep(0.7)
            if counter_green > 300:
                p_s.ChangeDutyCycle(10)
                time.sleep(0.5)
                counter_green = 0
            while ultraschall(0) > 30:
                if GPIO.input(13) == GPIO.HIGH:
                    break
                if GPIO.input(6) != GPIO.HIGH:
                    break
                value = ultraschall(1)
                time.sleep(0.1)
                if ultraschall(2) < 30:
                    p.ChangeDutyCycle(tempo)
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.HIGH)
                    p_s.ChangeDutyCycle(5.9)
                    time.sleep(1)
                    print("gefahr_green")
                    GPIO.output(in1,GPIO.HIGH)
                    GPIO.output(in2,GPIO.LOW)
                    p.ChangeDutyCycle(tempo)
                    p_s.ChangeDutyCycle(9)
                    time.sleep(1)
                if value > 20:
                    p_s.ChangeDutyCycle(7)
                if value < 10:
                    p_s.ChangeDutyCycle(10)
                else:
                    p_s.ChangeDutyCycle(8)
                
    else:
        counter_green == 0
    
    #Ausweichmannöver für die roten Steine
    if GPIO.input(5) == GPIO.HIGH:
        print("red")
        p.ChangeDutyCycle(tempo)
        while ultraschall(0) > 7:
            if GPIO.input(13) == GPIO.HIGH:
                break
            if GPIO.input(5) != GPIO.HIGH:
                break
            print("red" + str(counter_red))
            p_s.ChangeDutyCycle(10.4)
            counter_red = counter_red + 1
            if ultraschall(2) < 10:
                p.ChangeDutyCycle(tempo)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                p_s.ChangeDutyCycle(10.4)
    
                time.sleep(1)
                print("gefahr_red")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                p.ChangeDutyCycle(tempo)
                p_s.ChangeDutyCycle(5.9)
                time.sleep(1)
            if counter_red > 140:
                p_s.ChangeDutyCycle(5.9)
                time.sleep(1)
                counter_red = 0
                break

        while ultraschall(1) > 30:
            if GPIO.input(13) == GPIO.HIGH:
                break
            if GPIO.input(5) != GPIO.HIGH:
                break
            value = ultraschall(0)
            time.sleep(0.1)
            if ultraschall(2) < 10:
                p.ChangeDutyCycle(tempo)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                p_s.ChangeDutyCycle(10.4)

                time.sleep(1)
                print("gefahr_red")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                p.ChangeDutyCycle(tempo)
                p_s.ChangeDutyCycle(12)
                time.sleep(1)
            if value > 13:
                p_s.ChangeDutyCycle(6.7)
                print("hi")
            if value < 7:
                p_s.ChangeDutyCycle(10.7)
            else:
                p_s.ChangeDutyCycle(8)
    else:
        counter_red = 0

        
    #starte motor mit vorgegebener Geschwindigkeit
    p.ChangeDutyCycle(tempo)


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
    if counter >= 120:
        print("Ende")

        #warten bis alle ultraschall sensoren werte haben, sodass er weiß das er im End-Bereich steht, wenn ja stoppt er
        if ultraschall(2) <= 190 and ultraschall(2) >= 178 and mittelpunkt < 67:
            counter_2 = counter_2 + 1
            if counter_2 > 12:
                p.ChangeDutyCycle(0)
                print("Ende_Ende")
                while True:
                    pass
        else:
            counter_2 = 0


    #warte funktion, damit servo nicht sooft hintereinander lenken muss
    time.sleep(var_delay)

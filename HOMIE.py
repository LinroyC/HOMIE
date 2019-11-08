import RPi.GPIO as GPIO #GPIO through the rest of the script
import time             #Time module
GPIO.setwarnings(False) #Disable warning when configuring a script
GPIO.setmode(GPIO.BCM)  #Using GPIO numbers

#Setting up input channels
GPIO.setup(17, GPIO.IN)#PIR sensor for Front Door
GPIO.setup(18, GPIO.IN)#PIR sensor for Living Room
GPIO.setup(23, GPIO.IN)#PIR sensor for Bedroom

#Setting up output channels
GPIO.setup(26, GPIO.OUT)#LED output pin - Green - Home Secure
GPIO.setup(13, GPIO.OUT)#LED output pin - Red - Intruder Detected
GPIO.setup(22, GPIO.OUT)#LED output pin - Yellow - Movement Detected
GPIO.setup(24, GPIO.OUT)#Buzzer - Alarm

homeOwner = "Roy" #Homeowners username
homeOwner_pw = "pancakesallday" #Homeowners password
roy_ans1 = 'LE' #leaving
roy_ans2 = 'NE' #neither
roy_ans3 = 'RE' #returning

def Secure(): #Main function
    print (':)')
    print("")
    while True:
        frontDoor = GPIO.input(17)
        if frontDoor == 0:     #When output from motion sensor is LOW
            GPIO.output(13, 0) #Red LED OFF
            GPIO.output(26, 1) #Green LED ON
            GPIO.output(22, 0) #Yellow LED OFF
            time.sleep(1)
        elif frontDoor == 1: #When output from motion sensor is HIGH
            ID = input ("Identify yourself: ")
            PW = input ("Password: ")
            print("")
            if (homeOwner == ID and homeOwner_pw == PW):
                print ("Access Granted. Home is secure")
                print("")
                Q1 = input ("Hey, are you leaving or returning home?: ")
                if (roy_ans1 == Q1):
                    print ("Ok", ID,", i'll be here when you get back.")
                elif (roy_ans2 == Q1):
                    print ("Ok, let me know when you're ready to leave", ID,".")
                elif (roy_ans3 == Q1):
                    print ("Welcome Home", ID, ':)')
            else:
                print (':(')
                print("")
                print ("Intruder detected. Alarm sound will be activated.")
                print ("Standby while I detect movement . . .")
                print(""),frontDoor
                GPIO.output(26, 0) #Green LED OFF
                GPIO.output(13, 1) #Red LED ON
                GPIO.output(22, 0) #Yellow LED OFF
                GPIO.output(24, True)
                notSecure()

def notSecure(): #When home is not secure, the system will detect movement.
    while True:
        frontDoor = GPIO.input(17)
        livingRoom = GPIO.input(18)
        bedRoom = GPIO.input(23)
        if livingRoom == 1:#When output from motion sensor is HIGH
            print ("Movement detected in the Living Room.")
            print(""),livingRoom
            GPIO.output(22, 1)#Blink yellow LED - Movement Detected
            time.sleep(3)
            GPIO.output(22, 0)
        elif bedRoom == 1:#When output from motion sensor is HIGH
            print ("Movement detected in the Bedroom.")
            print ("")
            GPIO.output(22, 1)
            time.sleep(3)
            GPIO.output(22, 0)
        elif frontDoor == 1:#When output from motion sensor is HIGH
            print ("The intruder has left. I'll restart the system.")
            print ("")
            GPIO.output(22, 1)
            time.sleep(3)
            GPIO.output(26, 1)
            GPIO.output(22, 0)
            GPIO.output(13, 0)
            GPIO.output(24, False)
            Secure()
Secure()#Returns to the main function

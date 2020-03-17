import requests
import json
import datetime
import schedule
import time
import RPi.GPIO as GPIO
import time
#import pygame

#pygame.mixer.init()
#pygame.mixer.music.load('yes_epic.mp3')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

def timerMode(duration):
    try:
        test = int(duration)  
        if test > 0 and test <= 60:
            print("Valve is opening")
            #pygame.mixer.music.play()
            GPIO.output(18, GPIO.HIGH)                 
            
            for i in range(test):                           
                print(str(test - i) + " seconds remain")
                time.sleep(1)     
            print("Valve is closing")
            #pygame.mixer.music.stop()
        else:
            print("Out of bounds, needs to be 0-60 sec")
    except ValueError:
        print("Invalid Input, needs to be int")

    GPIO.output(18, GPIO.LOW)

# monitor db config table for changes
def monitor_id_change():
    original_id = retrieveID()
    print(original_id)

    while True:

        new_id = retrieveID()
        print(new_id)

        if new_id > original_id:
            original_id = new_id

            timerMode(retrieveDict().get("timer_length"))

        # check every 5 seconds
        time.sleep(5)
        
def retrieveID():
    my_dict = requests.get('http://35.194.80.240/config/recent').json()
    return my_dict['id']

def retrieveDict():
    return requests.get('http://35.194.80.240/config/recent').json()


monitor_id_change()







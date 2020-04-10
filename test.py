import requests
import json
import datetime
import schedule
import time
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

def timerMode(duration):
    try:
        test = int(duration)  
        if test > 0 and test <= 60:
            print("Valve is opening")
            GPIO.output(18, GPIO.HIGH)                 
            
            for i in range(test):                           
                print(str(test - i) + " seconds remain")
                time.sleep(1)     
            print("Valve is closing")
        else:
            print("Out of bounds, needs to be 0-60 sec")
    except ValueError:
        print("Invalid Input, needs to be int")

    GPIO.output(18, GPIO.LOW)
    
# TODO add threads
def startScheduledMode(days, startTimes, duration):
    scheduledMode(days.split(" "), startTimes.split(" "), duration)
    
    while(isNewID() == False):
        print("Waiting for scheduled time...")
        schedule.run_pending()
        time.sleep(1)
    

def scheduledMode(days, startTimes, duration):
     #if (len(days) != len(startTimes) or len(days) != len(durations)):
      #  print("Error, input argument count mismatch: days: {}, startTimes: {}, durations: {}".format(len(days), len(startTimes), len(durations)))
       # return 1

     for index in range(len(days)):
        if days[index] == "mon":
            #TODO: Check my syntax to make sure the .do(...) call is correct for the timer mode call
            schedule.every().monday.at(startTimes[index]).do(timerMode(duration))
        elif days[index] == "tues":
            schedule.every().tuesday.at(startTimes[index]).do(timerMode(duration))
        elif days[index] == "wed":
            schedule.every().wednesday.at(startTimes[index]).do(timerMode(duration))
        elif days[index] == "thurs":
            schedule.every().thursday.at(startTimes[index]).do(timerMode(duration))
        elif days[index] == "fri":
            print(startTimes[index])
            schedule.every().friday.at(startTimes[index]).do(timerMode(duration))
        elif days[index] == "sat":
            schedule.every().saturday.at(startTimes[index]).do(timerMode(duration))
        elif days[index] == "sun":
            schedule.every().sunday.at(startTimes[index]).do(timerMode(duration))
        else:
            print("Error, unknown day entry: days[{}] = {}".format(index, days[index]))
            return 2
    # No errors detected, all tasks should've been scheduled properly
     return 0

# monitor db config table for changes
def monitor_id_change():
    original_id = retrieveID()
    
    while True:
        new_id = retrieveID()
        print("Current ID = " + str(new_id) + ". Waiting for id = " + str(new_id+1))

        if new_id > original_id:        
            original_id = new_id
            
            config = retrieveDict()
        
            if config.get("mode_id") == "Timer Irrigation Mode":
                timerMode(config.get("timer_length"))
            elif config.get("mode_id") == "Scheduling Irrigation Mode":
                startScheduledMode(config.get("scheduled_days"), config.get("start_time"), config.get("timer_length"))
            elif config.get("mode_id") == "Adaptive Scheduling Mode":
                #TODO later
                print("Do ASM")
            else:
                #TODO later
                print("Do AIM")

        # check server every 5 seconds
        time.sleep(5)
   
def retrieveID():
    my_dict = requests.get('http://35.194.80.240/config/recent').json()
    return my_dict['id']

def retrieveDict():
    return requests.get('http://35.194.80.240/config/recent').json()


monitor_id_change()









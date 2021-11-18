import requests
import sys
import time
import grovepi

# sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

sys.path.append('/GrovePi-EE250/Software/Python')

from grovepi import *
from grove_rgb_lcd import *

import weather

PORT_BUZZER = 2     # D2
PORT_BUTTON = 4     # D4
ROTARY_SENSOR = 0   # A0

LCD_LINE_LEN = 16

# Setup
# pinMode(PORT_BUZZER, "OUTPUT")
# pinMode(PORT_BUTTON, "INPUT")
# pinMode(ROTARY_SENSOR, "INPUT")


while True:
    # get the current weather data and store it in variables
    curr_temp, curr_hum, curr_clouds, rain = weather.weather_init()
    print("current temp: " + str(curr_temp))
    print("current humidity: " + str(curr_hum))
    print("current cloud %: " + str(curr_clouds))
    print("current rain: " + str(rain))

    # do some signal processing to determine if it will rain or not


    # use thresholds to classify the day's heat level
    if curr_temp > 80:
        # really hot
        setRGB(252, 50, 43)
    elif curr_temp > 70:
        # kind of hot
        setRGB(255, 145, 0)
    elif curr_temp > 50:
        # warm-ish
        setRGB(255, 208, 0)
    elif curr_temp > 40:
        # cool
        setRGB(0, 255, 204)
    else:
        # cold!
        setRGB(0, 42, 255)


    # try:
        # checks if button has been pressed
        # if digitalRead(PORT_BUTTON):
        #     # BEEP!
        #     digitalWrite(PORT_BUZZER, 1)

        
        # time.sleep(0.1)

        # digitalWrite(PORT_BUZZER, 0)

        # if (ind == 0):
        #     # Display app name
        #     setText_norefresh(APPS[app]['name'])
        
        
        # # Scroll output
        # setText_norefresh('\n' + CACHE[app][ind:ind+LCD_LINE_LEN])
        # # TODO: Make the output scroll across the screen (should take 1-2 lines of code)
        # ind = (ind + 1)%(len(CACHE[app]))

        # rotary_value = analogRead(ROTARY_SENSOR) # reading rotary angle sensor value for mood lighting
        # if rotary_value < 205:
        #     setRGB(0, 0, 0) # off
        # elif rotary_value < 410:
        #     setRGB(64, 255, 83) # green
        # elif rotary_value < 615:
        #     setRGB(64, 172, 255) # blue
        # elif rotary_value < 820:
        #     setRGB(118, 64, 255) # purple
        # else:
        #     setRGB(249, 64, 255) # pink



    # except KeyboardInterrupt:
    #     # Gracefully shutdown on Ctrl-C
    #     setText('')
    #     setRGB(0, 0, 0)

    #     # Turn buzzer off just in case
    #     # digitalWrite(PORT_BUZZER, 0)

    #     break

    # except IOError as ioe:
    #     if str(ioe) == '121':
    #         # Retry after LCD error
    #         time.sleep(0.25)

    #     else:
    #         raise

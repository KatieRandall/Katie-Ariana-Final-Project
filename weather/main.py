import requests
import sys
import time

# sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

# from grovepi import *
# from grove_rgb_lcd import *

import weather

PORT_BUZZER = 2     # D2
PORT_BUTTON = 4     # D4
ROTARY_SENSOR = 0   # A0

LCD_LINE_LEN = 16

# Setup
# pinMode(PORT_BUZZER, "OUTPUT")
# pinMode(PORT_BUTTON, "INPUT")
# pinMode(ROTARY_SENSOR, "INPUT")

# Installed Apps!
APPS = [
    weather.WEATHER_APP
]

# Cache to store values so we save time and don't abuse the APIs
CACHE = ['']
CACHE[0] = '  ' + APPS[0]['init']()

app = 0     # Active app
ind = 0     # Output index

while True:
    print(CACHE[0])
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

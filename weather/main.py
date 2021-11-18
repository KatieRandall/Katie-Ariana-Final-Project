import requests
import sys
import time
import grovepi

# imports for matplotlib
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

sys.path.append('/GrovePi-EE250/Software/Python')

from grovepi import *
from grove_rgb_lcd import *

import weather

PORT_BUZZER = 2     # D2
PORT_BUTTON = 4     # D4
LIGHT_SENSOR = 0   # A0

LCD_LINE_LEN = 16

# Setup
# pinMode(PORT_BUZZER, "OUTPUT")
# pinMode(PORT_BUTTON, "INPUT")
pinMode(LIGHT_SENSOR, "INPUT")


def main():
    # get the current weather data and store it in variables
    curr_temp, curr_hum, curr_clouds, rain = weather.weather_init()
    print("current temp: " + str(curr_temp))
    print("current humidity: " + str(curr_hum))
    print("current cloud %: " + str(curr_clouds))
    print("current rain: " + str(rain))

    # do some signal processing

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


    # output the brightness in the room
    # lightVal = analogRead(LIGHT_SENSOR)
    # print
    # print("light value: " + str(lightVal))
    # print

    # matplotlib to plot light sensor data in real time

    
    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
    plt.show()


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


# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    # temp_c = round(tmp102.read_temp(), 2)
    currLight = analogRead(LIGHT_SENSOR)

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(currLight)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Light Values over Time')
    plt.ylabel('units')

if __name__ == "__main__":
    main()
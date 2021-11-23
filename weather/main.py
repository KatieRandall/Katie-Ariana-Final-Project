import requests
import sys
import time

import weather


def main():
    # get the current weather data and store it in variables
    curr_temp, curr_clouds, curr_uv, day = weather.weather_init()
    print("current temp: " + str(curr_temp))
    print("current cloud %: " + str(curr_clouds))
    print("current UV index " + str(curr_uv))
    print("daytime? " + str(day))

    
if __name__ == "__main__":
    main()

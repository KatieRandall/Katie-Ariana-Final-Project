# Our laptop will
# 1) publish weather data
# 2) subscribe to light sensor data from rpi

import paho.mqtt.client as mqtt
import time
import weather

# paths to use for topics
laptopdata_path = "arianang/data" #change to arianang/data if using ariana's pi
light_path = "arianang/light" #change to arianang/light if using ariana's pi

# global variable to create and update with current light sensor value
curr_lightsensor_val = 0

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # subscribing to the light sensor topic
    client.subscribe(light_path, qos=1)
    client.message_callback_add(light_path, light_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

# my custom callback for the light sensor
def light_callback(client, userdata, message):
    print("in light sensor callback")
    print("light sensor reading: " + str(message.payload, "utf-8"))

    # updating global variable
    curr_lightsensor_val = int(str(message.payload, "utf-8"))

    # do matplot lib here

# this function will take 3 parameters, the reading from the light sensor, a calculated light "score" from the API, and a boolean for if its day or not
# compare the outside light with the inside light and either open or shut the blinds. 
# very rudimentary at the moment, can implement things like lcd display changes, and opening blinds halfway or stuff like that later
def light_compare(sensor_lightvalue, api_lightvalue, api_daytime):
    if api_daytime == 1:
        # if it's daytime and it's brighter outside than inside, we want to open the blinds
        if api_lightvalue > sensor_lightvalue:
            blinds = "open blinds"
        # otherwise, we don't need the blinds to be open
        else:
            blinds = "close blinds"
    else:
        blinds = "close blinds"

    return blinds

# this function will take the information from the api and weight it to return one light value in a percentage out of 100
def api_signal_processing(api_cloudcover, api_uv):
    CLOUD_WEIGHT = 80 #using these weights for now but we will probably need to test some values to see what actual weights are
    UV_WEIGHT = 20
    MAX_UV_VALUE = 10
    uv_percent = api_uv / MAX_UV_VALUE

    # return outside light value out of 100
    return (CLOUD_WEIGHT*api_cloudcover + UV_WEIGHT*uv_percent)/1000

# this function returns the light sensor data in a percentage out of 100
def sensor_signal_processing(sensor_data):
    MAX_READING = 738 # max light sensor value

    # return inside light value out of 100
    return sensor_data / MAX_READING
    
if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        # getting current weather data
        curr_clouds, curr_uv, day_or_not = weather.weather_init()

        # calculating single value for outside light out of 100
        outside_lightval = api_signal_processing(curr_clouds, curr_uv)

        # calculating single value for inside light out of 100
        inside_lightval = sensor_signal_processing(curr_lightsensor_val)

        # publishing the result (open vs. closed blinds) to the pi
        result = light_compare(inside_lightval, outside_lightval, day_or_not)
        client.publish(laptopdata_path, str(result))
        
        time.sleep(0.5)
        

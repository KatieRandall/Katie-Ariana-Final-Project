# Our laptop will
# 1) publish weather data
# 2) subscribe to light sensor data from rpi

import paho.mqtt.client as mqtt
import time

light_path = "arianang/light" #change to arianang/light if using ariana's pi

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

    # do matplot lib here
    # below are notes from talking with Fayez

    # one way (this uses a lot of space though):
    # each time we get a value, append it to an array and erases first val
    # think of it like a circular buffer

    # better way
    # control when it polls for a new value
    # can change when i send light sensor value (maybe every 1000 ms)
    # poll every 1200-1300 ms (start with something larger)
    # keep one variable and overwrite it

    # if i know the time, do i need an array?
    # we know that mail will come (light sensor data will come) every 0.5 s
    # deposit in one variable and read it from that variable

#this function will take 3 parameters, the reading from the light sensor, a calculated light "score" from the API, and a boolean for if its day or not
#compare the outside ligth with the inside light and either open or shut the blinds. 
#very rudamentary at the moment, can implement things like lcd display changes, and opening blinds halfway or stuff like that later
def light_compare(sensor_lightvalue, api_lightvalue, api_daytime)
    if api_daytime:
        if api_lightvalue > sensor_data:
            open_blinds = TRUE
        else:
            open_blinds = FALSE
    else:
        open_binds = FALSE

#this function will take the information from the api and weight it to return one light value in a percentage out of 100
def api_signal_processing(api_cloudcover, api_uv):
    CLOUD_WEIGHT = 80 #using these weights for now but we will probably need to test some values to see what actual weights are
    UV_WEIGHT = 20
    MAX_UV_VALUE = 10
    uv_percent = api_uv / MAX_UV_VALUE

    #return outside light value out of 100
    return (COULD_WEIGHT*api_cloudcover + UV_WEIGHT*uv_percent)/1000

#this function returns the light sensor data in a percentage out of 100
def sensor_signal_processing(sensor_data):
    MAX_READING = 738 #max light sensor value

    #return inside light value out of 100
    return sensor_data / MAX_READING
    
if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        #publish the lcd color values to the pi every time the color needs to change. Probably need to add a callback for this
        #if lcd_changed:
        #    client.publish(light_path, payload=str(R_value)+ ","+str(G_value)+","+str(B_value),qos=1,retain=False)
        time.sleep(0.5)
        

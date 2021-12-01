# Our raspberry pi will
# 1) subscribe to weather data from laptop
# 2) publish light sensor data

import paho.mqtt.client as mqtt
import time
import grovepi  
from grovepi import *
from grove_rgb_lcd import *
import threading # has Lock, a key. you cannot perform operations without the key

lock = threading.Lock()

# paths to use for topics
laptopdata_path = "arianang/data" #change to arianang/data if using ariana's pi
light_path = "arianang/light" #change to arianang/light if using ariana's pi

# on_connect function to indicate whether we have connected to the broker successfully or not
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # subscribing to laptop data topic
    client.subscribe(laptopdata_path)
    client.message_callback_add(laptopdata_path, data_callback)

# default message callback
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

# laptop weather data callback 
def data_callback(client, userdata, message):
    with lock:
        print("in data callback")

        # sets the text on the LCD to open blinds or close blinds
        setText.no_refresh(str(message.payload, "utf-8"))
        if str(message.payload, "utf-8") == "open blinds":
            # to indicate that we should open the blinds, set background color to yellow
            setRGB(247, 255, 20)
        else:
            # to indicate that we should close the blinds, set background color to blue
            setRGB(20, 228, 255)


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    # setting up connections on the Grovepi
    light_sensor = 0 # light sensor should be plugged into A0
    pinMode(light_sensor,"INPUT")
    # lcd should be plugged into an I2C port. no code necessary to declare this, just wiring
    
    while True:
        try:
            with lock:
                # monitoring and publishing light sensor
                light_value = analogRead(light_sensor)
                client.publish(light_path, light_value)

            time.sleep(1)
            
        except IOError:
            print("error")

# Our raspberry pi will
# 1) subscribe to weather data from laptop
# 2) publish light sensor data

import paho.mqtt.client as mqtt
import time
from grovepi import *
from grove_rgb_lcd import *
import threading # has Lock, a key. you cannot perform operations without the key

lock = threading.Lock()

laptopdata_path = "arianang/data" #change to arianang/data if using ariana's pi
light_path = "arianang/light" #change to arianang/light if using ariana's pi

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # subscribing to laptop data topic
    client.subscribe(laptopdata_path)
    client.message_callback_add(laptopdata_path, data_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

# laptop weather data callback 
def data_callback(client, userdata, message):
    with lock:
        print("in data callback")

        # sets the text on the LCD to open blinds or close blinds
        setText(str(message.payload, "utf-8"))
        if str(message.payload, "utf-8") == "open blinds":
            # to indicate that we should open the blinds, set background color to yellow
            setRGB(247, 255, 20)
        else:
            # to indicate that we should close the blinds, set background color to blue
            setRGB(20, 228, 255)


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    # setting up connections on the Grovepi
    light_sensor = 0 # light sensor should be plugged into A0
    pinMode(light_sensor,"INPUT")
    
    while True:
        try:
            with lock:
                # monitoring and publishing light sensor
                light_value = analogRead(light_sensor)
                client.publish(light_path, str(light_value))

            time.sleep(.5)
            
        except IOError:
            print("error")

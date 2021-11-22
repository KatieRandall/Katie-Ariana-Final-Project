import paho.mqtt.client as mqtt
import time
from grovepi import *
from grove_rgb_lcd import *
import threading # has Lock, a key. you cannot perform operations without the key

lock = threading.Lock()

led_path = "kqrandal/led" #change to arianang/led if using ariana's pi

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # subscribing to led topic
    client.subscribe(led_path)
    client.message_callback_add(led_path, led_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#new led callback 
def led_callback(client, userdata, message):
    with lock:
        RGB = message.payload.split(".")
        setRGB(RGB[0], RGB[1], RGB[2])

# my custom callback for the led
# def led_callback(client, userdata, message):
    # with lock:
        # if str(message.payload, "utf-8") == "LED_ON":
            # # turn on LED
            # digitalWrite(led,1)
            # print ("LED on")
        # 
        # elif str(message.payload, "utf-8") == "LED_OFF":
            # # turn off LED
            # digitalWrite(led,0)
            # print ("LED off")



if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    # setting up up connections on the Grovepi
    light_sensor = 4
    pinMode(light_sensor,"INPUT")
    
    while True:
        try:
            with lock:
                # monitoring and publishing light sensor
                light_value = analogRead(light_sensor)
                client.publish(light_path, str(light_value))

            time.sleep(.5)
        except IOError:
            print("errror")

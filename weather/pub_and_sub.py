import paho.mqtt.client as mqtt
import time
from grovepi import *
from grove_rgb_lcd import *
import threading # has Lock, a key. you cannot perform operations without the key

lock = threading.Lock()

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # subscribing to led topic
    client.subscribe("arianang/led")
    client.message_callback_add("arianang/led", led_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

# my custom callback for the led
def led_callback(client, userdata, message):
    with lock:
        if str(message.payload, "utf-8") == "LED_ON":
            # turn on LED
            digitalWrite(led,1)
            print ("LED on")
        
        elif str(message.payload, "utf-8") == "LED_OFF":
            # turn off LED
            digitalWrite(led,0)
            print ("LED off")



if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    # setting up up connections on the Grovepi
    ultrasonic_ranger = 4
    led = 3
    button = 2
    pinMode(led,"OUTPUT")

    while True:
        with lock:
            # monitoring and publishing ultrasonic ranger
            ultrasonic_value = ultrasonicRead(ultrasonic_ranger)
            client.publish("arianang/ultrasonicRanger", str(ultrasonic_value))

        with lock:
            # monitoring button
            if digitalRead(button):
                client.publish("arianang/button", "Button pressed")

        time.sleep(1)
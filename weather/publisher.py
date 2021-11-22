import paho.mqtt.client as mqtt
import time
from pynput import keyboard
light_path = "kqrandal/light" #change to arianang/light if using ariana's pi

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

# def on_press(key):
    # try:
        # k = key.char # single-char keys
    # except:
        # k = key.name # other keys
    # 
    # if k == 'w':
        # print("w")
        # #send "w" character to rpi
        # client.publish("arianang/lcd", "w")
    # elif k == 'a':
        # print("a")
        # # send "a" character to rpi
        # # send "LED_ON"
        # client.publish("arianang/led", "LED_ON")
        # client.publish("arianang/lcd", "a")
    # elif k == 's':
        # print("s")
        # # send "s" character to rpi
        # client.publish("arianang/lcd", "s")
    # elif k == 'd':
        # print("d")
        # # send "d" character to rpi
        # # send "LED_OFF"
        # client.publish("arianang/led", "LED_OFF")
        # client.publish("arianang/lcd", "d")

if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
        #publish the lcd color values to the pi every time the color needs to change. Probably need to add a callback for this
        if lcd_changed:
            client.publish(light_path, payload=str(R_value)+ ","+str(G_value)+","+str(B_value),qos=1,retain=False)
            

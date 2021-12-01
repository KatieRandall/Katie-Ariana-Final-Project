# Our laptop will
# 1) publish weather data
# 2) subscribe to light sensor data from rpi

import paho.mqtt.client as mqtt
import time
import weather

# import statements for matplotlib
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# paths to use for topics
laptopdata_path = "arianang/data" #change to arianang/data if using ariana's pi
light_path = "arianang/light" #change to arianang/light if using ariana's pi

# global variable to create and update with current light sensor value
# we want this variable to be accessible in all functions, so we make it global
curr_lightsensor_val = 20 # initial value of 20 is arbitrary

# on_connect function to indicate whether we have connected to the broker successfully or not
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # subscribing to the light sensor topic
    client.subscribe(light_path, qos=1)
    client.message_callback_add(light_path, light_callback)

# default message callback
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

# custom callback for the light sensor
def light_callback(client, userdata, message):
    # if we are here, that means that our laptop has received light sensor data from our pi
    # our pi has published a light sensor value to a topic that we subscribe to
    print("in light sensor callback")
    print("light sensor reading: " + str(message.payload, "utf-8"))

    # updating global variable for light sensor value
    global curr_lightsensor_val
    curr_lightsensor_val = int(str(message.payload, "utf-8"))
    print("curr val in callback: " , curr_lightsensor_val)

# this function will take 3 parameters, the reading from the light sensor, a calculated light "score" from the API, and a boolean for if it's day or not
# compare the outside light (from API) with the inside light (from sensor) and either open or shut the blinds 
def light_compare(sensor_lightvalue, api_lightvalue, api_daytime):
    blinds = "" # we will end up returning this variable indicating whether to open or close the blinds
    if api_daytime == 1:
        # if it's daytime and it's brighter outside than inside, we want to open the blinds
        if api_lightvalue > sensor_lightvalue:
            blinds = "open blinds"
        # otherwise, we don't need the blinds to be open
        else:
            blinds = "close blinds"
    else:
        blinds = "close blinds"

    return blinds # we return a string

# this function will take the information from the API and weight it to return one light value in a percentage out of 100
def api_signal_processing(api_cloudcover, api_vis):
    #assigning weights
    CLOUD_WEIGHT = 80 
    VIS_WEIGHT = 20

    #converting visibility in units of km to visibility %
    MAX_VIS_VALUE = 296 #visibility (km) on a clear day
    vis_percent = api_vis / MAX_VIS_VALUE 

    # return outside light value out of 100 --> higher value = lighter
    return (CLOUD_WEIGHT*(100-api_cloudcover) + VIS_WEIGHT*vis_percent)/100

# this function returns the light sensor data in a percentage out of 100
def sensor_signal_processing(sensor_data):
    MAX_READING = 760 # max light sensor value (technically 800, but only goes to 760 on our sensor)

    # return inside light value out of 100 --> higher value = lighter
    return sensor_data / MAX_READING


# this function will be called every 1 second from main
# it pulls weather data and plots the light sensor data
def animate_sensorvals(i, xs, ys):

    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f')) # adding the current timestamp to the x-axis list
    ys.append(curr_lightsensor_val) # adding the current light sensor value to the y-axis list
    print(curr_lightsensor_val)

    # limit x and y lists to 20 items because we want our plot to only show the most recent 20 data points
    xs = xs[-20:]
    ys = ys[-20:]

    # draw x and y lists, plotting the points according to list contents
    ax.clear()
    ax.plot(xs, ys, marker = 'o', color = 'darkblue', alpha = 0.5)

    # formatting plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Light Sensor Readings over Time')
    plt.ylabel('Light Value')


    # getting current weather data by calling weather initialization function from weather.py
    curr_clouds, day_or_not, curr_vis = weather.weather_init()
    print("clouds: " + str(curr_clouds))
    print("visibility: " + str(curr_vis))
    print("day? " + str(day_or_not))

    # calculating single value for outside light out of 100
    outside_lightval = api_signal_processing(curr_clouds, curr_vis)

    # calculating single value for inside light out of 100
    inside_lightval = sensor_signal_processing(curr_lightsensor_val)

    # publishing the result (open vs. closed blinds) to the pi
    result = light_compare(inside_lightval, outside_lightval, day_or_not)
    client.publish(laptopdata_path, str(result))
    print("result should be: " + str(result))

    
if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start() # makes client listen on a different thread

    # creating plot for matplotlib of sensor data
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    # this line calls our animate_sensorvals function every 1 second, updating the plot on the screen
    animation = animation.FuncAnimation(fig, animate_sensorvals, fargs=(xs, ys), interval=1000)
    plt.show()
        

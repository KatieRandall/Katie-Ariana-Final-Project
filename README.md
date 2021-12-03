# EE 250 Final Project
### Ariana Goldstein and Katie Randall

___
Demonstration video link: https://drive.google.com/file/d/1feKb-XJO_jng_UeXqYVEznqVblJFk_Ti/view
___

## **Overview**
For our project, we created a small-scale prototype of a smart shade system that saves energy by indicating when to open and close the blinds (and therefore turn off and on the lights) depending on the brightness levels in the room and outside.

Our program directly senses the brightness of the room using the GrovePi light sensor. It also pulls weather data— specifically, cloud cover percentage and visibility— to calculate a comparable brightness value of the outdoors. Based on the comparison of these values, the GrovePi LCD screen indicates whether the blinds should be open or closed to let in natural light, and in turn, whether the lights should be switched on or off.

The real-world applications of this project are significant. A similar system could be implemented in homes, offices, and school buildings to minimize the time that lights must be switched on, maximizing efficiency and minimizing energy use. The concept of using a combination of indoor sensors and outdoor brightness data to toggle window blinds has lots of potential utilizations. We wanted to explore the basics in our project.

The sections below provide technical details about how our program can be run.
___

## **External Libraries Used**
In order to orchestrate our Grovepi sensing, we used the Grovepi library. Ensure that this library is installed before running the program. To create the constantly updating plot of the incoming light sensor data, we used the Matplotlib library. This library must be installed on your laptop/VM.
```
pip install matplotlib
```

We also used the Paho MQTT library for our MQTT connection. This library must be installed on both your laptop/VM and Raspberry Pi.
```
pip install paho-mqtt
```

___

## **To Compile and Execute**
Once you have the external libraries installed, clone this repository to both a laptop/VM and a Raspberry Pi so that you have local copies of all of the necessary files. In both terminals, run
```
git clone git@github.com:KatieRandall/Katie-Ariana-Final-Project.git
```
The two files that must be executed to demonstrate our project are `laptop_pub_and_sub.py` and `rpi_pub_and_sub.py`. They must be executed on the laptop/VM and Raspberry Pi correspondingly.

On your laptop, in the terminal, run
```
python3 laptop_pub_and_sub.py
```

On your Pi, in the terminal, run
```
python3 rpi_pub_and_sub.py
```

Once both of these commands have been executed, the two nodes will communicate via MQTT. The laptop will pull data from the Weather API and publish it to the Pi, and the Pi will sense light data from the environment and publish it to the laptop. 

A plot should pop up and begin plotting the light sensor data live, updating each second depending on the current brightness condition of the room.
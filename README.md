# EE 250 Final Project
### Ariana Goldstein and Katie Randall

Demonstration video link:

## **Overview**

## **To Compile and Execute**
Begin by cloning this repository to both a laptop/VM and a Raspberry Pi so that you have local copies of all of the necessary files. In both terminals, run
```
git clone git@github.com:KatieRandall/Katie-Ariana-Final-Project.git
```
The two files that must be executed to demonstrate our project are `laptop_pub_amd_sub.py` and `rpi_pub_and_sub.py`. They must be executed on the laptop/VM and Raspberry Pi correspondingly.

On your laptop, in the terminal, run
```
python3 laptop_pub_amd_sub.py
```

On your Pi, in the terminal, run
```
python3 rpi_pub_amd_sub.py
```

Once both of these commands have been executed, the two nodes will communicate via MQTT. The laptop will pull data from the Weather API and publish it to the Pi, and the Pi will sense light data from the environment and publish it to the laptop. 


## **External Libraries Used**
In order to orchestrate our Grovepi sensing, we used the Grovepi library. To create the constantly updating plot of the incoming light sensor data, we used the Matplotlib library. We also used the Paho MQTT library for our MQTT connection.

Before running, you need to install these libraries.
```
pip install matplotlib
```
```
pip install paho-mqtt
```
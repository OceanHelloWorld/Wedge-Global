# Wedge-Global
Software Development for Wedge Global.
Codes are for private company use.

## Video Input Device
Raspberry Pi Camera
https://www.raspberrypi.org/documentation/hardware/camera/README.md

## Microprocessor before transmission
Raspberry Pi
Powered: 5V, 2.5A
Using OpenCV and Python code to send a signal to the communication device when the yokohama is not in sight.

## Communication
LoRaWan using The Internet Things network
### LoRaWan: Rx bandwidth: 500-125 kHz; Data Rate: 290 bps - 50 Kbps; Max Output Power: 20 dBm; Battery lifetime - 2000mAh: 9=~ 9 years; Link Budget 154 dB; Security: Yes
Lora RF bandwidth in Europe: 868 MHz

## Receiving Device
Build an app that sends a twitt when we receive a signal from the Lora network
Using Twitter's Twython API: https://twython.readthedocs.io/en/latest/
Receive a tweet when a the yokohama is out of sight, then the operator will go check.



## Background Information
Based on the average sun rise and set time of the island, it will be too dark for us to monitor from 7:00 pm to 7:30 am. However, only 11pm to 5am is high tide that we need to worry about. In this period, 4am to 8am has the highest waves being the most dangerous point of the day.
http://www.tides4fishing.com/es/islas-canarias/las-palmas-de-gran-canaria

## Step 1
load raspberry pi with Raspbian image

## Step 2
Install Git on Raspberry Pi
https://projects.raspberrypi.org/en/projects/getting-started-with-git/4

## Step 3
git clone https://github.com/OceanHelloWorld/Wedge-Global.git

## Step 4
Follow Sigfox instruciton
https://github.com/SNOC/rpisigfox

## Step 5
Follow OpenCV install instruction
https://resources.sigfox.com/document/errorwarning-status-events-api-endpoints-explanation

## Step 6
Register the SigFox portal
https://backend.sigfox.com/cms/section/52f8a5b593368ce020b924e1/info

## Step 7
Setup Callbacks or other API funcitons
https://resources.sigfox.com/document/errorwarning-status-events-api-endpoints-explanation

## Step 8
Run the code from Wedge-Global repo




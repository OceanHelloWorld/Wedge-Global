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



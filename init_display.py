#!/usr/bin/python3

# direwatch

"""
Craig Lamparter KM6LYW,  2021, MIT Licnese

Code derived from Adafruit PIL python example

This will tail a direwolf log file and display callsigns on an
adafruit st7789 tft display (https://www.adafruit.com/product/4484).
Follow the instructions here to get the driver/library loaded:

https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-setup

Current configuration is for the 240x240 st7789 unit.

Do not install the kernel module/framebuffer.

GPIO pins 12 (PTT) and 16 (DCD) are monitored and light green/red icons respectively.
Configure these gpio pins in direwolf.


Installation on raspbian/buster for short-attentions span programmers like me:

sudo apt-get install python3-pip   # python >= 3.6 required
sudo pip3 install adafruit-circuitpython-rgb-display
sudo pip3 install pyinotify
sudo apt-get install python3-dev python3-rpi.gpio
vi /boot/config.txt  # uncomment following line: "dtparam=spi=on"
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py   ## this gets the digitalio python module
sudo pip install aprslib     ## so we can parse ax.25 packets

Much code taken from ladyada for her great work driving these devices,
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

modified by W4MHI February 2022
- separate display initialization
"""

import digitalio
import board
import threading
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import RPi.GPIO as GPIO

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
#reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Use one and only one of these screen definitions:
## half height adafruit screen 1.1" (240x135), two buttons
#disp = st7789.ST7789(
#    board.SPI(),
#    cs=cs_pin,
#    dc=dc_pin,
##    rst=reset_pin,
#    baudrate=BAUDRATE,
#    width=135,
#    height=240,
#    x_offset=53,
#    y_offset=40,
#    rotation=270,
#)

# full height adafruit screen 1.3" (240x240), two buttons
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
#    rst=reset_pin,
    baudrate=BAUDRATE,
    height=240,
    y_offset=80,
    rotation=0
)

# don't write to display concurrently with thread
display_lock = threading.Lock()

# Create image and drawing object
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

image = Image.new("RGBA", (width, height))
draw = ImageDraw.Draw(image)

#!/usr/bin/python3

# direwatch

"""
Craig Lamparter KM6LYW,  2021, MIT License

modified by W4MHI February 2022
- see the init_display.py module for display settings
- see https://www.delftstack.com/howto/python/get-ip-address-python/ for the ip address
"""

import sys
import argparse
import time
from netifaces import interfaces, ifaddresses, AF_INET

sys.path.insert(0, '/home/pi/common')
from display_util import *
from constants import *

def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--fontsize", required=False, help="Font size for messages")
    ap.add_argument("-b", "--big", required=False, help="large text to display")
    ap.add_argument("-s", "--small", required=False, help="smaller text underneath")
    args = vars(ap.parse_args())
    return args

args = parse_arguments()

if args["fontsize"]:
   fontsize = int(args["fontsize"])
   if fontsize > 34:
      print("The input: " + str(fontsize) + " is greater than: 34 that is maximum value supported.")
      print("Setting to maximum value: 34.")
      fontsize = 34
   elif fontsize < 20:
      print("The input: " + str(fontsize) + " is lower than: 20 that is minimum value supported.")
      print("Setting to minimum value: 20.")
      fontsize = 20
else:
   print("Setting font size to default value: 24.")
   fontsize = 24

if args["big"]:
   message_big = args["big"]
else:
   message_big = "DigiPi"

if args["small"]:
   message_small = args["small"]
else:
   message_small = "DigiPi Operational!"

# title
font_title = get_titlefont()

# define writing fonts
font_message = get_writingfont(fontsize)
spacing = get_spacing(fontsize)
last_line = get_lastline(fontsize)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill="#000000")

# title bar
draw.rectangle((0, 0, width, TITLE_BAR_H), outline=0, fill="#333333")
draw.text((10, 0) , TITLE, font=font_title, fill="#888888")

# ip addresses message
count = 1
draw.text((PAD_LEFT, count*spacing), "Net's IP Addresses", font=font_message, fill="#00FF00")

first_pass = True
ip_present = False
while ip_present == False:
   count = 1
   # ip addresses
   for ifaceName in interfaces():
      for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP yet'}]):
         if ifaceName.startswith("wlan") or ifaceName.startswith("eth"):
            # increment for interface name
            count = count + 1
            if first_pass:
               # show the interface name
               draw.text((PAD_LEFT, count*spacing), "[" + ifaceName  + "]", font=font_message, fill="#00FF00")

            # increment for the ip address
            count = count + 1
            #delete the previous line if exists
            draw.rectangle((0, count*spacing, width, (count+1)*spacing), outline=0, fill="#000000")
            draw.text((4*PAD_LEFT, count*spacing), i['addr'], font=font_message, fill="#00FF00")

            if i['addr'].startswith('No IP') == False:
               ip_present = True
   disp.image(image)
   first_pass = False
   # wait and re-iterate if no ip address
   if ip_present == False:
      time.sleep(3)

# message
count = count + 1
if last_line >= count:
  draw.text((PAD_LEFT, last_line*spacing), message_small, font=font_message, fill="#FFFF00")

#with display_lock:
disp.image(image)

print("DigiPi operational!\n")
exit(0)


#!/usr/bin/python3

# direwatch

"""
Craig Lamparter KM6LYW,  2021, MIT License

modified by W4MHI February 2022
- see the init_display.py module for display settings
- see https://www.delftstack.com/howto/python/get-ip-address-python/ for the ip address
"""

import argparse
import os
import socket
from init_display import *

# define some constants to help with graphics layout
padding = 4
title_bar_height = 34

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--fontsize", required=False, help="Font size for callsigns")
    ap.add_argument("-b", "--big", required=False, help="large text to display")
    ap.add_argument("-s", "--small", required=False, help="smaller text underneath")
    args = vars(ap.parse_args())
    return args

args = parse_arguments()

if args["fontsize"]:
   # 17 puts 11 lines 2 columns
   # 20 puts 9 lines
   # 25 puts 7 lines
   # 30 puts 6 lines   ** default
   # 34 puts 5 lines, max width
   fontsize = int(args["fontsize"])
   if fontsize > 30:
      print("Look, this display isn't very wide, the maximum font size is 34pts, and you chose " + str(fontsize) + "?")
      print("Setting to 34 instead.")
      fontsize = 34
else:
   fontsize = 30

if args["big"]:
   message_big = args["big"]
else:
   message_big = "DigiPi"

if args["small"]:
   message_small = args["small"]
else:
   message_small = "Operational!"


font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
line_height = font.getsize("ABCJQ")[1] - 1          # tallest callsign, with dangling J/Q tails
#max_line_width = font.getsize("   KN6MUC-15")[0] - 1   # longest callsign i can think of in pixels, with spaces for symbol
#max_cols = width // max_line_width
font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
font_huge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)

# Draw a black filled box to clear the image.
#draw.rectangle((0, 0, width, height), outline=0, fill=0)
draw.rectangle((0, 0, width, height), outline=0, fill="#000000")
draw.rectangle((0, 0, width, 30), outline=0, fill="#333333")

# title bar
draw.text((10, 0) , "DigiPi", font=font_big, fill="#888888")

# message
draw.text((10, height * .33 + font.getsize("MMM")[1] + 8), message_small, font=font, fill="#666666")

# ip address
draw.text((10, height * .33 ), extract_ip(), font=font_big, fill="#888888")
print("DigiPi operational!\n")

#with display_lock:
disp.image(image)

exit(0)

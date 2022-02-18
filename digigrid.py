#!/usr/bin/python3

# direwatch

"""
Craig Lamparter KM6LYW,  2021, MIT License

GpsPoller Written by Dan Mandle http://dan.mandle.me September 2012
License: GPL 2.0

modified by W4MHI February 2022
- see the init_display.py module for display settings
- see https://gpsd.gitlab.io/gpsd/gpsd_json.html for json format
- see https://github.com/space-physics/maidenhead for maidenhead grid
- install 'pip install maidenhead'
"""

import time
import threading
import maidenhead as mh
from gps import *
from init_display import *

def timer(timeout):
  pad_str = ' ' * len('%d' % timeout)
  for i in range(timeout, 0, -1):
    sys.stdout.write('GPS reading in %d seconds %s\r' % (i, pad_str),)
    sys.stdout.flush()
    time.sleep(1)

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    try:
      while gpsp.running:
        self.current_value = gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
    except StopIteration:
      pass

if __name__ == '__main__':
  # define some constants to help with graphics layout
  padding = 4
  title_bar_height = 34
  fontsize = 30

  font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
  line_height = font.getsize("ABCJQ")[1] - 1          # tallest callsign, with dangling J/Q tails
  font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
  font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

  # Draw a black filled box to clear the image.
  draw.rectangle((0, 0, width, height), outline=0, fill="#000000")
  draw.rectangle((0, 0, width, 30), outline=0, fill="#333333")

  # title bar
  draw.text((10, 0) , "DigiPi GPS", font=font_big, fill="#888888")

  gpsd = None #seting the global variable
  gpsp = GpsPoller() # create the thread
  gpsp.start() # start it up

  # refresh the data at every # seconds
  timer(3)
  gpsp.running = False
  gpsp.join() # wait for the thread to finish what it's doing
  print ("Done. Display results...")

  # display the gps data + grid
  height = font.getsize("MMM")[1] + 6
  lat = str(float("{0:.4f}".format(gpsd.fix.latitude)))
  lon = str(float("{0:.4f}".format(gpsd.fix.longitude)))
  alt = str(float("{0:.2f}".format(gpsd.fix.altitude/.3048)))
  utc = datetime.fromisoformat(str(gpsd.fix.time).replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')

  draw.text((5, 1*height), "UTC: "+ utc, font=font_small, fill="#888888")
  draw.text((5, 2*height), "LAT: " + lat, font=font_big, fill="#888888")
  draw.text((5, 3*height), "LON: " + lon, font=font_big, fill="#888888")
  draw.text((5, 4*height), "ALT: " + alt, font=font_big, fill="#888888")
  draw.text((5, 5*height), "FIX: " + str(gpsd.fix.mode) + "D", font=font_big, fill="#888888")
  draw.text((5, 6*height), "GRID: " + mh.to_maiden(gpsd.fix.latitude, gpsd.fix.longitude), font=font_big, fill="#888888")

  disp.image(image)
  print("Exiting.")


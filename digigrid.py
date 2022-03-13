#!/usr/bin/python3
# digigrid

"""
Mihai W4MHI,  2022, MIT License

synopsis:
Print at DigiPi screen the GPS coordinates and Maidenhead grid.
"""
import sys
import threading
import argparse
from datetime import datetime
from gps import *

sys.path.insert(0, '/home/pi/common')
from constants import *
from display_util import *
from time_util import *

try:
    import maidenhead
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install maidenhead")

def parse_arguments():
  ap = argparse.ArgumentParser()
  ap.add_argument("-c", "--continous", required=False, help="Continous running. True/False")
  ap.add_argument("-r", "--refresh", required=False, help="GPS data refresh. Default is the minimum value of 3, the maximum value is 60, in seconds.")
  ap.add_argument("-d", "--debug", required=False, help="GPS data printed to the console for debugging purpose. True/False")
  args = vars(ap.parse_args())
  return args

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.session = gps(mode=WATCH_ENABLE)
    self.current_value = None
    self.running = True

  def get_current_value(self):
    return self.current_value

  def run(self):
    try:
      while self.running:
        self.current_value = self.session.next()
    except StopIteration:
      pass

if __name__ == '__main__':
  # debug flag
  debug = False

  # type of running
  continous = False

  # refresh time
  refresh_time = 3

  # painted screen flag
  painted_screen = False

  # sum control for refresh
  old = new = 0

  args = parse_arguments()

  if(args["continous"]):
    continous = bool(args["continous"])

  if(args["debug"]):
    debug = bool(args["debug"])

  if(args["refresh"]):
    refresh_time = int(args["refresh"])

  if(refresh_time < 2):
    print("Input value is lower than the minimum acceptable (3s). Refresh time set to 3 seconds.")
    refresh_time = 3

  if(refresh_time > 60):
    print("Input value is higher than the maximum acceptable (60s). Refresh time set to 60 seconds.")
    refresh_time = 60

  # title
  font_title = get_titlefont()

  # define writing fonts
  fontsize = 28
  font_message = get_writingfont(fontsize)
  spacing = get_spacing(fontsize)

  # Draw a black filled box to clear the image.
  draw.rectangle((0, 0, width, height), outline=0, fill="#000000")

  # title bar
  draw.rectangle((0, 0, width, TITLE_BAR_H), outline=0, fill="#333333")
  draw.text((10, 0) , TITLE + "GPS [" + str(refresh_time) + "s]", font=font_title, fill="#888888")

  # create the thread
  gpsp = GpsPoller()

  try:
    gpsp.start()

    while True:
      # default data
      utc_d = 'NaN'
      utc_t = 'NaN'
      lat = 'NaN'
      lon = 'NaN'
      alt = 'NaN'
      fix = 'NaN'
      grid = 'NaN'

      report = gpsp.get_current_value()
      isvalidreport = report != None and 'epx' in list(report.keys())
      if (isvalidreport):
        lat = str(float("{0:.4f}".format(report.lat)))
        lon = str(float("{0:.4f}".format(report.lon)))
        alt = str(float("{0:.2f}".format(report.alt/.3048)))
        utc_d = datetime.fromisoformat(str(report.time).replace('Z', '+00:00')).strftime('%Y-%m-%d')
        utc_t = datetime.fromisoformat(str(report.time).replace('Z', '+00:00')).strftime('%H:%M:%S')
        fix = str(report.mode) + "D"
        grid = maidenhead.to_maiden(report.lat, report.lon)
        new = hash("[" +  str(float("{0:.2f}".format(report.lat))) + "]:[" + str(float("{0:.2f}".format(report.lon))) + "]:["+ str(float("{0:.0f}".format(report.alt))) + "]")

      if(report != None and old != new):
        old = new
        print("Refresh display, new data")
        # Draw a black filled box to clear the image.
        draw.rectangle((0, spacing, width, height), outline=0, fill="#000000")
        disp.image(image)

        # display the gps data + grid
        draw.text((5, 1*spacing), "UTC: "+ utc_d, font=font_message, fill="#00FF00")
        draw.text((5, 2*spacing), "UTC: "+ utc_t, font=font_message, fill="#00FF00")
        draw.text((5, 3*spacing), "LAT: " + lat + "°", font=font_message, fill="#FFFF00")
        draw.text((5, 4*spacing), "LON: " + lon + "°", font=font_message, fill="#FFFF00")
        draw.text((5, 5*spacing), "ALT: " + alt + "ft", font=font_message, fill="#0000FF")
        draw.text((5, 6*spacing), "FIX: " + fix, font=font_message, fill="#888888")
        draw.text((5, 7*spacing), "GRID: " + grid, font=font_message, fill="#FF0000")

      if(painted_screen == False):
        # Draw a black filled box to clear the image.
        draw.rectangle((0, spacing, width, height), outline=0, fill="#000000")
        disp.image(image)

        # warning for the waiting time
        draw.text((5, 1*spacing), "Waiting for data...", font=font_message, fill="#00FF00")
        draw.text((5, 2*spacing), str(refresh_time) + "s", font=font_message, fill="#FFFF00")

        # no need another warning
        painted_screen = True

      disp.image(image)

      # debug
      if(debug and isvalidreport):
        print("---------------GPS reading---------------")
        print("latitude    " , report.lat)
        print("longitude   " , report.lon)
        print("time utc    " , report.time)
        print("altitude (m)" , report.alt)
        print("eps         " , report.eps)
        print("epx         " , report.epx)
        print("epv         " , report.epv)
        print("ept         " , report.ept)
        print("speed (m/s) " , report.speed)
        print("climb       " , report.climb)
        print("mode        " , report.mode)
      else:
        print("Waiting for data...")

      if(continous == False and isvalidreport):
        gpsp.running = False
        gpsp.join()
        break

      # refresh the data at every # seconds
      timer(refresh_time)
  except (KeyboardInterrupt, SystemExit):
    print ("The thread ended.")
    gpsp.running = False
    gpsp.join()

  print("Done. Exiting.")


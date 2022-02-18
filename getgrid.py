#! /usr/bin/python

'''
Written by Dan Mandle http://dan.mandle.me September 2012
License: GPL 2.0

modified by W4MHI February 2022
- see https://gpsd.gitlab.io/gpsd/gpsd_json.html for json format
- see https://github.com/space-physics/maidenhead for maidenhead grid
- install 'pip install maidenhead'
'''

import os
import time
import threading
from gps import *
import maidenhead as mh

gpsd = None #seting the global variable

os.system('clear') #clear the terminal (optional)

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
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:

      # refresh the data at every # seconds
      timer(3)

      # display the gps data + grid
      print('----------------------------------------')
      print('latitude     ', gpsd.fix.latitude)
      print('longitude    ', gpsd.fix.longitude)
      print('time utc     ', gpsd.fix.time)
      print('altitude  (m)', float("{0:.2f}".format(gpsd.fix.altitude)))
      print('altitude (ft)', float("{0:.2f}".format(gpsd.fix.altitude/.3048)))
      print('mode  (2D/3D)', gpsd.fix.mode)
      print('grid         ', mh.to_maiden(gpsd.fix.latitude, gpsd.fix.longitude))
      print

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print("\nKilling Thread...")
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print("Done.\nExiting.")

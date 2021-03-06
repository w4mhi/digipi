#!/usr/bin/python3

# direwatch

"""
Craig Lamparter KM6LYW,  2021, MIT Licnese

modified by W4MHI February 2022
- see the init_display.py module for display settings
"""
import sys
import argparse
import time
import subprocess
import re
import pyinotify
import RPi.GPIO as GPIO
import threading
import signal
import os
import aprslib

sys.path.insert(0, '/home/pi/common')
from display_util import *

# define some constants to help with graphics layout
padding = 4
title_bar_height = 34

def signal_handler(signal, frame):
   print("Got ", signal, " exiting.")
   draw.rectangle((0, 0, width, height), outline=0, fill=(30,30,30))
   with display_lock:
       disp.image(image)
   #sys.exit(0)  # thread ignores this
   os._exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-l", "--log", required=True, help="Direwolf log file location")
    ap.add_argument("-f", "--fontsize", required=False, help="Font size for callsigns")
    ap.add_argument("-t", "--title_text", required=False, help="Text displayed in title bar")
    ap.add_argument("-o", "--one", action='store_true', required=False, help="Show one station at a time full screen")
    args = vars(ap.parse_args())
    return args

args = parse_arguments()
logfile = args["log"]
if args["fontsize"]:
   # 30 puts 6 lines
   # 33 puts 5 lines, max width
   fontsize = int(args["fontsize"])
   if fontsize > 33:
      print("Look, this display isn't very wide, the maximum font size is 33pts, and you chose " + str(fontsize) + "?")
      print("Setting to 33 instead.")
      fontsize = 33
else:
   fontsize = 30   # default 30
if args["title_text"]:
   title_text = args["title_text"]
else:
   title_text = "Direwatch"

# Bluetooth LED connection check

def bluetooth_connection_poll_thread():
    bt_status = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)

    while True:
        cmd = "hcitool con | wc -l"
        connection_count = subprocess.check_output(cmd, shell=True).decode("utf-8")
        if int(connection_count) > 1:
            if bt_status == 0:
                bt_status = 1
                print("BT ON")
                bticon = Image.open('bt.small.on.png')
                GPIO.output(5, GPIO.HIGH)
                image.paste(bticon, (width - title_bar_height * 3 + 12  , padding + 2 ), bticon)
                with display_lock:
                    disp.image(image)
        else:
            if bt_status == 1:
                bt_status = 0
                bticon = Image.open('bt.small.off.png')
                GPIO.output(5, GPIO.LOW)
                image.paste(bticon, (width - title_bar_height * 3 + 12  , padding + 2 ), bticon)
                with display_lock:
                    disp.image(image)
        time.sleep(2)

bluetooth_thread = threading.Thread(target=bluetooth_connection_poll_thread, name="btwatch")
bluetooth_thread.start()


# Status LEDs thread

def handle_changeG(cb):
   with open('/sys/class/gpio/gpio16/value', 'r') as f:          ## GREEN
      status = f.read(1)
      if status == '0':
         draw.ellipse(( width - title_bar_height, padding, width - padding * 2, title_bar_height - padding), fill=(0,80,0,0))
      else:
         draw.ellipse(( width - title_bar_height, padding, width - padding * 2, title_bar_height - padding), fill=(0,200,0,0))
      with display_lock:
         disp.image(image)
   f.close

def handle_changeR(cb):
   with open('/sys/class/gpio/gpio12/value', 'r') as f:          ## RED
      status = f.read(1)
      if status == '0':
         draw.ellipse(( width - title_bar_height * 2, padding, width - title_bar_height - padding * 2 , title_bar_height - padding), fill=(80,0,0,0))
      else:
         draw.ellipse(( width - title_bar_height * 2, padding, width - title_bar_height - padding * 2 , title_bar_height - padding), fill=(200,0,0,0))
         pass
      with display_lock:
         disp.image(image)
   f.close

def null_function(junk):  # default callback prints tons of debugging info
   return()

# Instanciate a new WatchManager (will be used to store watches).
wmG = pyinotify.WatchManager()
wmR = pyinotify.WatchManager()

# Associate this WatchManager with a Notifier
notifierG = pyinotify.Notifier(wmG, default_proc_fun=null_function)
notifierR = pyinotify.Notifier(wmR, default_proc_fun=null_function)

# Watch both gpio pins for change
wmG.add_watch('/sys/class/gpio/gpio16/value', pyinotify.IN_MODIFY)
wmR.add_watch('/sys/class/gpio/gpio12/value', pyinotify.IN_MODIFY)

#Setup threads
watch_threadG = threading.Thread(target=notifierG.loop, name="led-watcherG", kwargs=dict(callback=handle_changeG))
watch_threadR = threading.Thread(target=notifierR.loop, name="led-watcherR", kwargs=dict(callback=handle_changeR))
#Start threads after we display our logo, etc, much farther down in the code
#watch_threadG.start()
#watch_threadR.start()

# Load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
fontname = "DejaVuSans.ttf"
fontname_bold = "DejaVuSans-Bold.ttf"
if os.path.exists("/usr/share/fonts/truetype/dejavu/" + fontname):
   fontpath = "/usr/share/fonts/truetype/dejavu/" + fontname
elif os.path.exists("./" + fontname):
   fontpath = "./" + fontname
else:
   print("Couldn't find font " +  fontname + " in working dir or /usr/share/fonts/truetype/dejavu/")
   exit(1)
if os.path.exists("/usr/share/fonts/truetype/dejavu/" + fontname_bold):
   fontpath_bold = "/usr/share/fonts/truetype/dejavu/" + fontname_bold
elif os.path.exists("./" + fontname_bold):
   fontpath_bold = "./" + fontname_bold
else:
   print("Couldn't find font " +  fontname_bold + " in working dir or /usr/share/fonts/truetype/dejavu/")
   exit(1)
font = ImageFont.truetype(fontpath, fontsize)
font_big = ImageFont.truetype(fontpath_bold, 24)
font_huge = ImageFont.truetype(fontpath_bold, 34)
font_epic = ImageFont.truetype(fontpath, 40)
#font = ImageFont.truetype("/usr/share/fonts/truetype/dafont/BebasNeue-Regular.ttf", fontsize)
#font_big = ImageFont.truetype("/usr/share/fonts/truetype/dafont/BebasNeue-Regular.ttf", 24)
#font_huge = ImageFont.truetype("/usr/share/fonts/truetype/dafont/BebasNeue-Regular.ttf", 34)
line_height = font.getsize("ABCJQ")[1] - 1          # tallest callsign, with dangling J/Q tails

# load and scale symbol chart based on font height
symbol_chart0x64 = Image.open("aprs-symbols-64-0.png")
symbol_chart1x64 = Image.open("aprs-symbols-64-1.png")
fontvertical = font.getsize("XXX")[1]
symbol_chart0x64.thumbnail(((fontvertical + fontvertical // 8) * 16, (fontvertical + fontvertical // 8) * 6)) # nudge larger than font, into space between lines
symbol_chart1x64.thumbnail(((fontvertical + fontvertical // 8) * 16, (fontvertical + fontvertical // 8) * 6)) # nudge larger than font, into space between lines
symbol_dimension = symbol_chart0x64.width//16

max_line_width = font.getsize("KN6MUC-15")[0] + symbol_dimension + (symbol_dimension // 8)   # longest callsign i can think of in pixels, plus symbo width + space
max_cols = width // max_line_width

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill="#000000")

# Draw our logo
w,h = font.getsize(title_text)
draw.text((padding * 3,  height // 2 - h) ,   title_text, font=font_huge,   fill="#99AA99")
with display_lock:
    disp.image(image)
time.sleep(1)

# erase the screen
draw.rectangle((0, 0, width, height), outline=0, fill="#000000")

# draw the header bar
draw.rectangle((0, 0, width, title_bar_height), fill=(30, 30, 30))
draw.text((padding, padding), title_text, font=font_big, fill="#99AA99")

# draw the bluetooth icon
bticon = Image.open('bt.small.off.png')
image.paste(bticon, (width - title_bar_height * 3 + 12  , padding + 2 ), bticon)

# draw Green LED
draw.ellipse(( width - title_bar_height               , padding,       width - padding * 2,                  title_bar_height - padding), fill=(0,80,0,0))

# draw Red LED
draw.ellipse(( width - title_bar_height * 2           , padding,    width - title_bar_height - padding * 2 , title_bar_height - padding), fill=(80,0,0,0))

with display_lock:
    disp.image(image)

# fire up green/red led threads
watch_threadG.start()
watch_threadR.start()

call = "null"
x = padding
max_lines  = ( height - title_bar_height - padding )  //   line_height
max_cols = ( width // max_line_width )
line_count = 0
col_count = 0

# tail and block on the log file
f = subprocess.Popen(['tail','-F',logfile], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#f = subprocess.Popen(['tail','-F','-n','80','/run/direwolf.log'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)  # debug

##### one_loop() ############
def one_loop():
   symbol_chart0x64 = Image.open("aprs-symbols-64-0.png")
   symbol_chart1x64 = Image.open("aprs-symbols-64-1.png")
   while True:
      line = f.stdout.readline().decode("utf-8", errors="ignore")

      search = re.search("^\[\d\.\d\] (.*)", line)
      if search is not None:
         packetstring = search.group(1)
         packetstring = packetstring.replace('<0x0d>','\x0d').replace('<0x1c>','\x1c').replace('<0x1e>','\x1e').replace('<0x1f>','\0x1f')
      else:
         continue
      try:                                        #   aprslib has trouble parsing all packets
         packet = aprslib.parse(packetstring)
         call = packet['from']
         if 'symbol' in packet:
            symbol = packet['symbol']
            symbol_table = packet['symbol_table']
         else:
            symbol = '/'
            symbol_table = '/'
      except:               #   aprslib has trouble parsing all packets
         continue

      symbol_dimension = 64
      offset = ord(symbol) - 33
      row = offset // 16
      col = offset % 16
      y = height // 3
      x = width // 3
      draw.rectangle((0, title_bar_height, width, height), outline=0, fill="#000000")  # erase most of screen
      crop_area = (col*symbol_dimension, row*symbol_dimension, col*symbol_dimension+symbol_dimension, row*symbol_dimension+symbol_dimension)
      if symbol_table == '/':
         symbolimage = symbol_chart0x64.crop(crop_area)
      else:
         symbolimage = symbol_chart1x64.crop(crop_area)
      symbolimage = symbolimage.resize((height // 2, height // 2), Image.NEAREST)
      image.paste(symbolimage, (0, 36), symbolimage)
      draw.text((5, height - font_epic.getsize("X")[1] - 3), call, font=font_epic, fill="#AAAAAA") # text up from bottom edge

      with display_lock:
          disp.image(image)
      time.sleep(1)


##### list_loop() ############
def list_loop():
  call = "null"
  # position cursor in -1 slot, as the first thing the loop does is increment slot
  y = padding + title_bar_height - font.getsize("ABCJQ")[1]
  x = padding
  max_lines  = ( height - title_bar_height - padding )  //   line_height
  max_cols = ( width // max_line_width )
  line_count = 0
  col_count = 0

  while True:
    line = f.stdout.readline().decode("utf-8", errors="ignore")

    search = re.search("^\[\d\.\d\] (.*)", line)
    if search is not None:
       packetstring = search.group(1)
       packetstring = packetstring.replace('<0x0d>','\x0d').replace('<0x1c>','\x1c').replace('<0x1e>','\x1e').replace('<0x1f>','\0x1f')
    else:
       continue

    lastcall = call

    try:                                        #   aprslib has trouble parsing all packets
       packet = aprslib.parse(packetstring)
       call = packet['from']
       if 'symbol' in packet:
          symbol = packet['symbol']
          symbol_table = packet['symbol_table']
       else:
          symbol = '/'
          symbol_table = '/'
    except:                                     #   if it fails, let's just snag the callsign
       #print("aprslib failed to parse.")
       search = re.search("^\[\d\.\d\] ([a-zA-Z0-9-]*)", line)
       if search is not None:
          call = search.group(1)
          symbol = '/'
          symbol_table = '/'
       else:
          continue

    offset = ord(symbol) - 33
    row = offset // 16
    col = offset % 16

    if call == lastcall:   # blink duplicates
       time.sleep(0.5)
       draw.text((x + symbol_dimension + (symbol_dimension // 8) , y), call, font=font, fill="#000000") # start text after symbol, relative padding
       with display_lock:
           disp.image(image)
       time.sleep(0.1)
       draw.text((x + symbol_dimension + (symbol_dimension // 8) , y), call, font=font, fill="#AAAAAA") # start text after symbol, relative padding
       with display_lock:
           disp.image(image)
    else:
       y += line_height
       if line_count == max_lines:       # about to write off bottom edge of screen
           col_count += 1
           x = col_count * max_line_width
           y = padding + title_bar_height
           line_count = 0
       if col_count == max_cols:         # about to write off right edge of screen
           x = padding
           y = padding + title_bar_height
           draw.rectangle((0, title_bar_height + 1, width, height), outline=0, fill="#000000") # erase lines
           line_count = 0
           col_count = 0
           time.sleep(2.0)
       crop_area = (col*symbol_dimension, row*symbol_dimension, col*symbol_dimension+symbol_dimension, row*symbol_dimension+symbol_dimension)
       if symbol_table == '/':
          symbolimage = symbol_chart0x64.crop(crop_area)
       else:
          symbolimage = symbol_chart1x64.crop(crop_area)
       image.paste(symbolimage, (x, y), symbolimage)
       draw.text((x + symbol_dimension + (symbol_dimension // 8) , y), call, font=font, fill="#AAAAAA") # start text after symbol, relative padding
       line_count += 1
       with display_lock:
           disp.image(image)

if args["one"]:
   one_loop()
else:
   list_loop()


exit(0)

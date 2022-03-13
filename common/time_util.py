#!/usr/bin/python3

"""
Mihai W4MHI,  2022, MIT License
"""
import sys
import time
from datetime import datetime

def timer(timeout):
  pad_str = ' ' * len('%d' % timeout)
  for i in range(timeout, 0, -1):
    sys.stdout.write('New data in %d seconds %s\r' % (i, pad_str),)
    sys.stdout.flush()
    time.sleep(1)
  print("\n")

def time_converter(time):
  converted_time = datetime.fromtimestamp(
    int(time)
  ).strftime('%I:%M %p')
  return converted_time
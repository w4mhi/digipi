#!/usr/bin/python3

"""
W4MHI February 2022, MIT License
"""
from PIL import ImageFont

# define some constants to help with graphics layout
PAD_LEFT = 4
TITLE_BAR_H = 34
TITLE = "DigiPi "

# font 34pts - 6 lines of text
# font 32pts - 6 lines of text
# font 30pts - 6 lines of text
# font 28pts - 7 lines of text
# font 26pts - 7 lines of text
# font 24pts - 7 lines of text
# font 22pts - 8 lines of text
# font 20pts - 8 lines of text

def get_writingfont(fontsize):
  return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)

def get_titlefont():
  return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)

def get_weatherfont(fontsize):
  return ImageFont.truetype('/usr/share/fonts/truetype/weather/weathericons-regular-webfont.ttf', fontsize - 2)

def get_spacing(fontsize):
  fontused = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
  if fontsize == 34:
    return fontused.getsize("XZMQ")[1] + 4
  elif fontsize == 32:
    return fontused.getsize("XZMQ")[1] + 0.5
  elif fontsize == 30:
    return fontused.getsize("XZMQ")[1] + 2.5
  elif fontsize == 28:
    return fontused.getsize("XZMQ")[1] + 0.25
  elif fontsize == 26:
     return fontused.getsize("XZMQ")[1] + 2.5
  elif fontsize == 24:
    return fontused.getsize("XZMQ")[1] + 4.5
  elif fontsize == 22:
    return fontused.getsize("XZMQ")[1] + 3
  elif fontsize == 20:
    return fontused.getsize("XZMQ")[1] + 5.5
  else:
    return fontused.getsize("XZMQ")[1] + 4

def get_lastline(fontsize):
  if fontsize == 34:
    return 5
  elif fontsize == 32:
    return 6
  elif fontsize == 30:
    return 6
  elif fontsize == 28:
    return 7
  elif fontsize == 26:
    return 7
  elif fontsize == 24:
    return 7
  elif fontsize == 22:
    return 8
  elif fontsize == 20:
    return 8
  else:
    return 9

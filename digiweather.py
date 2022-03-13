#!/usr/bin/python3
# digiweather

"""
Mihai W4MHI,  2022, MIT License

- see the display_util.py module for display settings
- see config.ini for weather configuration
"""
import sys
import time
import argparse
from PIL import ImageFont

sys.path.insert(0, '/home/pi/common')
from constants import *
from display_util import *
from time_util import *
from weather_util import *

def show_main(wicon, temp, condition):
  # big image, temperature, conditions
  image.paste(wicon, (PAD_LEFT, TITLE_BAR_H + 6), wicon)

  if(freezing):
    draw.text((PAD_LEFT, 6*spacing), temp, font=font_message, fill="#0000FF")
  elif(hot):
    draw.text((PAD_LEFT, 6*spacing), temp, font=font_message, fill="#FF0000")
  else:
    draw.text((PAD_LEFT, 6*spacing), temp, font=font_message, fill="#FFFF00")

  draw.text((PAD_LEFT, 7*spacing), condition, font=font_message, fill="#FFFF00")

def show_details(wicon, temp_min, temp_max, humidity, pressure, wind_speed, sunrise, sunset):
  # reduce image
  wicon = wicon.reduce(2)
  image.paste(wicon, (width - 125, TITLE_BAR_H + 6), wicon)

  draw.text((PAD_LEFT, 1*spacing), "\uf055", font=font_weather, fill = "#0000FF")
  draw.text((PAD_LEFT_W, 1*spacing), temp_min, font=font_message, fill="#0000FF")

  draw.text((PAD_LEFT, 2*spacing), "\uf055", font=font_weather, fill = "#FF0000")
  draw.text((PAD_LEFT_W, 2*spacing), temp_max, font=font_message, fill="#FF0000")

  draw.text((PAD_LEFT, 3*spacing), "\uf07A", font=font_weather, fill = "#00FF00")
  draw.text((PAD_LEFT_W, 3*spacing), humidity, font=font_message, fill = "#00FF00")

  draw.text((PAD_LEFT, 4*spacing), "\uf079", font=font_weather, fill = "#00FF00")
  draw.text((PAD_LEFT_W, 4*spacing), pressure, font=font_message, fill="#00FF00")

  draw.text((PAD_LEFT, 5*spacing), get_wind_icon("NE"), font=font_weather, fill = "#00FF00")
  draw.text((PAD_LEFT_W, 5*spacing), wind_speed, font=font_message, fill="#00FF00")

  draw.text((PAD_LEFT, 6*spacing), "\uf046", font=font_weather, fill = "#FFFF00")
  draw.text((PAD_LEFT_W, 6*spacing), sunrise, font=font_message, fill = "#FFFF00")

  draw.text((PAD_LEFT, 7*spacing), "\uf047", font=font_weather, fill = "#FFFF00")
  draw.text((PAD_LEFT_W, 7*spacing), sunset, font=font_message, fill = "#FFFF00")

def parse_arguments():
  ap = argparse.ArgumentParser()
  ap.add_argument("-c", "--continous", required=False, help="Continous running. True/False")
  ap.add_argument("-r", "--refresh", required=False, help="Weather data refresh. Default is the minimum value of 600, the maximum value is 3600, in seconds.")
  ap.add_argument("-f", "--flip", required=False, help="Screen data refresh between data. Default is the minimum value of 5, the maximum value is 30, in seconds.")
  ap.add_argument("-d", "--debug", required=False, help="Weather data printed to the console for debugging purpose. True/False")
  args = vars(ap.parse_args())
  return args

if __name__ == '__main__':
  # debug flag
  debug = False

  # type of running
  continous = False

  # refresh time
  refresh_screen = 5
  refresh_time = 900

  args = parse_arguments()

  if(args["continous"]):
    continous = bool(args["continous"])

  if(args["refresh"]):
    refresh_time = int(args["refresh"])

  if(refresh_time < 600):
    print("Input value is lower than the minimum acceptable (600s = 10min). Refresh time set to 900 seconds (15 min).")
    refresh_time = 900

  if(refresh_time > 3600):
    print("Input value is higher than the maximum acceptable (3600s = 1h). Refresh time set to 900 seconds (15 min).")
    refresh_time = 900

  if(args["flip"]):
    refresh_time = int(args["flip"])

  if(refresh_screen < 4):
    print("Input value is lower than the minimum acceptable 5s. Refresh time set to 5 seconds.")
    refresh_screen = 5

  if(refresh_screen > 30):
    print("Input value is higher than the maximum acceptable 30s. Refresh time set to 30s.")
    refresh_screen = 30

  # config file
  FREEZING_TEMP = get_freezing_temp()
  HOT_TEMP = get_hot_temp()

  # title
  font_title = get_titlefont()

  # define writing fonts
  fontsize = 26
  font_message = get_writingfont(fontsize)
  spacing = get_spacing(fontsize)
  font_weather = get_weatherfont(fontsize)
  
  # special font left padding
  wd = font_weather.getsize("\uf000")[0]
  PAD_LEFT_W = PAD_LEFT + wd + 6

  # Draw a black filled box to clear the image.
  draw.rectangle((0, 0, width, height), outline=0, fill="#000000")

  # title bar
  draw.rectangle((0, 0, width, TITLE_BAR_H), outline=0, fill="#333333")
  draw.text((10, 0) , TITLE + "WEATHER", font=font_title, fill="#888888")

  while True:
    try:
      weather = get_weather()

      if(debug):
        print("----------" + time.strftime("%H:%M [%a %d-%b-%y]") + "----------")
        print(weather)

      main = get_data(weather, "main")

      temperature = get_data(main, "temp")
      temp = u"temp: {:.1f}°".format(temperature)

      temperature_min = get_data(main, "temp_min")
      temp_min = u"{:.1f}°".format(temperature_min)
      temperature_max = get_data(main, "temp_max")
      temp_max = u"{:.1f}°".format(temperature_max)

      freezing = False
      hot = False
      if(temperature <= FREEZING_TEMP):
        freezing = True

      if(temperature >= HOT_TEMP):
        hot = True

      pressure = get_data(main, "pressure")
      pressure = "{:.2f}inHg".format(pressure*0.03)

      humidity = get_data(main, "humidity")
      humidity = u"{:.0f}%".format(humidity)

      wind = get_data(weather, "wind")
      wind_speed = get_data(wind, "speed")
      wind_deg = get_data(wind, "deg")
      wind_direction = get_wind_direction(wind_deg)
      wind_speed = wind_direction + u"{:.1f}mph".format(wind_speed)

      wsys = get_data(weather, "sys")
      sunrise = get_data(wsys, "sunrise")
      sunset = get_data(wsys, "sunset")

      sun_rise = "{}".format(time_converter(sunrise))
      sun_set = "{}".format(time_converter(sunset))

      conditions = get_data(weather, "weather")  
      condition = get_data(conditions[0], "description")
      weather_icon = get_data(conditions[0], "icon")

      # open image
      wicon = Image.open("weather/" + weather_icon + ".png")

      # flip screen
      while True:
        # erase the screen
        draw.rectangle((0, TITLE_BAR_H, width, height), outline = 0, fill = "#000000")
        show_main(wicon, temp, condition)
        disp.image(image)

        # refresh after sleep
        time.sleep(refresh_screen)
        refresh_time = refresh_time - refresh_screen

        # erase the screen
        draw.rectangle((0, TITLE_BAR_H, width, height), outline = 0, fill = "#000000")
        show_details(wicon, temp_min, temp_max, humidity, pressure, wind_speed, sun_rise, sun_set)
        disp.image(image)

        # refresh after sleep
        time.sleep(refresh_screen)
        refresh_time = refresh_time - refresh_screen

        if(refresh_time <= 0 or continous == False):
          break

    except (KeyboardInterrupt, SystemExit):
      print ("The thread ended.")
      break

    if(continous == False):
      break

print("Done. Exiting.")

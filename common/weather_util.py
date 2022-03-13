#!/usr/bin/python3

"""
Mihai W4MHI,  2022, MIT License
"""
try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

try:
    import json
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install json")

try:
    import configparser
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install configparser")

def get_api_key():
  config = configparser.ConfigParser()
  config.read('config/weather.ini')
  return config['openweathermap']['API_KEY']

def get_address():
  config = configparser.ConfigParser()
  config.read('config/weather.ini')
  return config['openweathermap']['CITY']+","+config['openweathermap']['COUNTRYCODE']

def get_freezing_temp():
  config = configparser.ConfigParser()
  config.read('config/weather.ini')
  return float(config['temp']['FREEZING'])

def get_hot_temp():
  config = configparser.ConfigParser()
  config.read('config/weather.ini')
  return float(config['temp']['HOT'])

def get_weather():
  base = "http://api.openweathermap.org/data/2.5/weather?"
  uri = base+"appid="+get_api_key()+"&q="+get_address()+"&units=imperial"
  print(uri)

  response = requests.get(uri)
  if(response.status_code==200):
    json_data = json.loads(response.text)
    return json_data
  return {}

def get_data(dataset, key):
  try:
    return dataset[key]
  except KeyError as e:
    print("Data key " + key + " is missing!")
    return 0

def get_wind_direction(deg):
  wind_direction = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", "N"]
  index = int(deg/22.5)
  return wind_direction[index]

def get_wind_icon(direction):
  if(direction == "N"):
    return "\uf05C"
  if(direction == "S"):
    return "\uf060"
  if(direction == "E"):
    return "\uf059"
  if(direction == "W"):
    return "\uf061"
  if(direction == "NE"):
    return "\uf05A"
  if(direction == "NW"):
    return "\uf05B"
  if(direction == "SE"):
    return "\uf05D"
  if(direction == "SW"):
    return "\uf05E"
  else:
    return "\u0050"
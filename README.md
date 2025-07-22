Overview
===============
The DigiPi project can be seen at http://craiger.org/digipi/
In this repository are modified files or additional files to the project.
Clone the repository with command `https://github.com/w4mhi/digipi.git`, then `cd digipi` to get access to the files.

`Release note:` 
- copy the files from `bash` folder to the parent folder `/home/pi`.
- copy folders `common` and `config` in `/home/pi`.
- verify the files digiweather.py have executable rights.

Use the command `chmod +x digiweather.py` for example. Do the same for `weather.sh`

## DigiWeather
This program will show information from the weather in the desired location. The location is configured in the `configuration` folder.
Copy the font from `fonts` to a permanent location with `sudo cp weathericons-regular-webfont.ttf /usr/share/fonts/truetype/weather/weathericons-regular-webfont.ttf`.

The `weather.ini` has couple of parameters that can be changed. The <weather-api-key> can be requested for free from https://openweathermap.org/api

Run the file with the python command `digiweather.py`.

Command line parameters:
`"-c", "--continous"`   - optional parameter used for continous running. Accepted values: `True/False"`

`"-r", "--refresh"`     - optional parameter used for GPS data refresh. Default is the minimum value of 3, the maximum value is 60, in seconds.

`"-f", "--flip"`        - optional parameter used to refresh the screen data between the overview and detailed weather information. Default is the minimum value of 5, the maximum value is 30, in seconds.

`"-d", "--debug"`       - optional parameter used to print the GPS data to the console for debugging purpose. Accepted values: `True/False"`

Thank you for trying the files and the original project!
73!



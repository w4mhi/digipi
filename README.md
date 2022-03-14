Overview
===============
The DigiPi project can be seen at http://craiger.org/digipi/
In this repository are modified files or additional files to the project.
Clone the repository with command `https://github.com/w4mhi/digipi.git`, then `cd digipi` to get access to the files.

DigiBanner has a new look, so it needs to run at boot without being overwritten by the DigiPi TNC.
The following changes needs to be made in the `/etc/rc.local`.
* `sudo remount`
* `sudo nano /etc/rc.local`
* look for `/home/pi/digibanner.py -b DigiPi -s "     v1.6" &` and add 4 spaces (that will align better the version with title)
* prefix the line `service tnc start` with `#` (practically comment the line)

`Release note:` copy the files from `digipi` folder to the parent folder `/home/pi`. Same with the `common` and `config` folder. Veify the files digi*.py have executable rights.
If they are not execuatble, use the command `chmod +x direwatch.py` for example.

## DigiGrid
This program will show some information from the GPS including the Maidehead Grid.
The assumption is the DigiPi is connected to a GPS source, like ICOM-705 with the USB OUT setup to GPS Data.

The program has dependency on the Maidenhead module.
* `sudo remount` to make the file system writeable.
* `pip3 install maidenhead` will install the module in a folder that is not in the path.
* save changes from the DigiPi

The following steps are to verify if the operator has GPS data. All commands require RasPi shell.

Check if services are working:
> `systemctl is-active gpsd`
> `systemctl is-active chronyd`

Check data with `cgps -s`.

If data doesn't show on the screen, restart the services with the following commands. For authentication choose `1` and use the `pi` account password.
> `systemctl stop gpsd.socket`
> `systemctl stop gpsd`
> `systemctl start gpsd`
> `systemctl start gpsd.socket`

Verify the data is present with `cgps -s`.

Run the file with the python command `python3 digigrid.py`.

Command line parameters:
`"-c", "--continous"`   - optional parameter used for continous running. Accepted values: `True/False"`
`"-r", "--refresh"`     - optional parameter used for GPS data refresh. Default is the minimum value of 3, the maximum value is 60, in seconds.
`"-d", "--debug"`       - optional parameter used to print the GPS data to the console for debugging purpose. Accepted values: `True/False"`

## DigiWeather
This program will show some information from the weather in the desired location. The location is configured in the `configuration` folder.
Copy the font from `fonts` to a permanent location with `sudo cp weathericons-regular-webfont.ttf /usr/share/fonts/truetype/weather/weathericons-regular-webfont.ttf`.

The `weather.ini` has couple of parameters that can be changed. The <weather-api-key> can be requested for free from https://openweathermap.org/api

Run the file with the python command `python3 digiweather.py`.

Command line parameters:
`"-c", "--continous"`   - optional parameter used for continous running. Accepted values: `True/False"`
`"-r", "--refresh"`     - optional parameter used for GPS data refresh. Default is the minimum value of 3, the maximum value is 60, in seconds.
`"-f", "--flip"`        - optional parameter used to refresh the screen data between the overview and detailed weather information. Default is the minimum value of 5, the maximum value is 30, in seconds.
`"-d", "--debug"`       - optional parameter used to print the GPS data to the console for debugging purpose. Accepted values: `True/False"`

## Installation
The GPS grid can be installed in the main dashboard of the DigiPi as a service.
* copy the `bash` folder to the `/home/pi` per `Release notes`.
* give executable rights with `sudo chmod +x weather.sh` and `sudo chmod +x gpsgrid.sh`
* create a new service, for example `gpsgrid` by running `sudo nano /etc/systemd/system/gpsgrid.service`
* add the following lines:

```console
[Unit]
Description=GPS and Maidenhead Grid for Pi

[Service]
ExecStartPre=+systemctl stop fldigi sstv wsjtx tnc300b digipeater tnc node js8call
ExecStart=/home/pi/gpsgrid.sh
User=pi
Restart=no

[Install]
WantedBy=multi-user.target
```

`Note:` The ExecStartPre section will stop all current services to let the current service to run.

* change the service permissions to 644 with `sudo chmod 644 /etc/systemd/system/gpsgrid.service`
* enable the service `sudo systemctl enable gpsgrid.service`
* reload the daemon for services `sudo systemctl daemon-reload`
* edit the `index.php` to add the service to the dashboard with `sudo nano /var/www/html/index.php`
* look for a similar section and insert the following one

```php
if (isset($_POST["gpsgrid"])) {
    $submit = $_POST["gpsgrid"];
    if ( $submit == 'on' ) {
        $output = shell_exec('sudo systemctl start gpsgrid');
        sleep(5);
        echo $output;
    }
    if ( $submit == 'off' ) {
        $output = shell_exec('sudo systemctl stop gpsgrid');
        echo $output;
    }
}
```

* navigate down in the file code until the similar section is met and insert the following code:
    
```php
#-- GPS GRID -------------------------------------------------
echo "<tr>";
$output = shell_exec('systemctl is-active gpsgrid');
#$output = str_replace("failed", "inactive", $output);
$output = chop($output);
if ($output == "active")
{
    echo '<td bgcolor="lightgreen">';
}
elseif ($output == "failed")
{
    echo '<td bgcolor="lightgreen">';
}
else
{
    echo '<td bgcolor="lightgrey">';
}
echo "&nbsp;";
echo "</td><td>";
echo "<font size=+1>GPS & Maidenhead Grid</font></td>";
echo '<td align="right" nowrap>';
echo '<input type="submit" name="gpsgrid" value="on"> ';
echo '<input type="submit" name="gpsgrid" value="off">';
echo "</font>";
echo "</td></tr>";
```

* find where the service are called for shutdown and insert the followingcode:
    
```php
$output = shell_exec('sudo systemctl reset-failed gpsgrid');
```

* restart the DigiPi with `sudo reboot` to make sure the system is in the read-only mode

## Documentation for debugging
- see the init_display.py module for display settings
- see https://gpsd.gitlab.io/gpsd/gpsd_json.html for json format
- see https://github.com/space-physics/maidenhead for maidenhead grid
- see for GpsPoller: https://github.com/timmyreilly/BumpyRoads/blob/master/RaspberryPiFiles
-              https://stackoverflow.com/questions/6146131/python-gps-module-reading-latest-gps-data
-              http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
- see for service under RasPi https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f
- also https://www.thedigitalpictureframe.com/ultimate-guide-systemd-autostart-scripts-raspberry-pi/

Thank you for trying the files and the original project!
73!



# DigiPi Project

The DigiPi project enhances the original DigiPi (see [project site](http://craiger.org/digipi/)) with additional and modified files.  
Clone this repository with:

```sh
git clone https://github.com/w4mhi/digipi.git
cd digipi
```

## Release Notes

- Copy files from the `bash` folder to `/home/pi`.
- Copy the `common` and `config` folders to `/home/pi`.

---

## Backup & Restore

The `backup` folder contains scripts for backing up and restoring DigiPi configurations.

**Typical workflow:**
1. Set up Wi-Fi and SSH into your DigiPi.
2. Use the backup script to save the original files (e.g., `/home/pi/backup/clean`).
3. Configure DigiPi at [http://digipi.local/](http://digipi.local/).

**To re-configure:**
1. Use the backup script to save your current config (e.g., `/home/pi/backup/IC-705` for IC-705).
2. Restore original files and delete `/var/cache/digipi/localized.txt`.
3. Reconfigure DigiPi as needed.
4. Use the backup script again for new configurations (e.g., `/home/pi/backup/alinco` for Alinco).

---

## DigiWeather

DigiWeather displays weather information for a configured location.

### Setup

1. Copy the font from `fonts`:
   ```sh
   sudo cp weathericons-regular-webfont.ttf /usr/share/fonts/truetype/weather/weathericons-regular-webfont.ttf
   ```
2. Ensure `digiweather.py` and `weather.sh` are executable:
   ```sh
   chmod +x digiweather.py weather.sh
   ```
3. Edit `weather.ini` to set parameters.  
   Obtain a free API key from [OpenWeatherMap](https://openweathermap.org/api).

### Usage

Run DigiWeather with:
```sh
python digiweather.py
```

#### Command Line Parameters

- `-c`, `--continous` : Run continuously (`True`/`False`)
- `-r`, `--refresh`   : GPS data refresh interval (3–60 seconds, default: 3)
- `-f`, `--flip`      : Screen refresh interval (5–30 seconds, default: 5)
- `-d`, `--debug`     : Print GPS data for debugging (`True`/`False`)

---

Thank you for trying these files and supporting the original project!  
**73!**



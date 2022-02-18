# digipi
Files for the DigiPi project made by Craig Lamparter 

The project can be seen at http://craiger.org/digipi/
In this repository are modified files or additional files to the project.

1. NEW: init_display.py
This file is a split from the digibanner.py and direwatch.py. It initialize the display and is just a module that was separated for easier management of the display.
The line 'rotation = 0' is changed from the original 'rotation = 180' to accomodate the USB HAT on the Raspberry Pi Zero 2 and add the possibility of a Pi-Sugar UPS. The device will stand-up with the switches up and the display would need rotation 0.

2. MODIFIED: digibanner.py
This file is just separated from the display initialization and includes that module. It adds the IP address on the screen, useful when the opeartor wants to know it. It can be ran from the shell with the command:
    python3 digibanner.py

3. MODIFIED: direwatch.py
This file is just separated from the display initialization and includes that module. 

4. NEW: digigrid.py
Derived from the digibanner.py will show some information from the GPS including the Maidehead Grid.
This program assumes the operator has ICOM-705 and the USB OUT setup to GPS Data. Here are some steps to verify if the operator has GPS data. All commands require shell.

Check if services are working:
    systemctl is-active gpsd
    systemctl is-active chronyd

Check data with:
    cgps -s

Run the file with the python command:
 python3 digigrid.py

Thank you for trying the files and the original project!
73!



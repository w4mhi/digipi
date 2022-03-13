#!/bin/bash
# trap ctrl-c and call ctrl_c()
trap ctrl_c INT
trap ctrl_c TERM
function ctrl_c() {
   echo "CTRL-C pressed, killing digigrid"
   exit 0
}

/home/pi/digigrid.py -c true

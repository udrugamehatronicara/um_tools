#!/bin/bash

sudo busybox devmem 0x0c303018 w 0x458
sudo busybox devmem 0x0c303010 w 0x400

sudo modprobe can
sudo modprobe can_raw
sudo modprobe mttcan

sudo ip link set can0 up type can bitrate 500000 dbitrate 1000000 berr-reporting on fd on
#sudo ip link set can0 up type can bitrate 125000 dbitrate 300000 berr-reporting on fd on

#sudo ip link set can0 up type can bitrate 250000 dbitrate 500000 berr-reporting on fd on
sudo ip link set can0 up
sudo ifconfig can0 up
#sudo ip link set can0 up type can bitrate 125000

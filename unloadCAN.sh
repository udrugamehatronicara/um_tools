#!/bin/bash

sudo modprobe --remove-dependencies -f mttcan
sudo modprobe --remove-dependencies -f can_raw
sudo modprobe --remove-dependencies -f can

sudo ifconfig can0 down
sudo ip link set can0 down
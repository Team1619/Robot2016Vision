#!/bin/sh

wait 25
v4l2-ctl -c exposure_auto=1 -c exposure_absolute=5 -c backlight_compensation=0 -c sharpness=50 -c brightness=30 -c contrast=5
/home/ubuntu/Robot2016/visionPoster.py

#!/bin/sh

wait 5
v4l2-ctl -c brightness=133 -c sharpness=50 -c backlight_compensation=0 -c exposure_auto=1 -c exposure_absolute=10
/home/ubuntu/Robot2016/visionPoster.py 

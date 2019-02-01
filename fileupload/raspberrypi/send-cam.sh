#!/bin/bash

raspistill -o /tmp/photo.jpg -w 400 -h 300 -q 5 -n -t 1
python3 sakuraio-upload.py /tmp/photo.jpg


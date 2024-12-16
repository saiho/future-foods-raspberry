#!/bin/bash -e

root_dir=$(dirname "$0")/..

ssh pi@raspberrypi.local sudo systemctl stop future-foods-sensor
ssh pi@raspberrypi.local sudo mount -o remount,rw /app
ssh pi@raspberrypi.local rm -rf /app/future-foods/lib /app/future-foods/__pycache__
rsync -rlt --progress $root_dir/app/ --exclude=__pycache__/ pi@raspberrypi.local:/app/future-foods
ssh pi@raspberrypi.local py3compile /app/future-foods
ssh pi@raspberrypi.local sudo mount -o remount,ro /app

if [[ "$1" == "--start" ]]; then
	ssh pi@raspberrypi.local sudo systemctl start future-foods-sensor
fi

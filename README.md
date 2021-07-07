This is a very draft project for handling the sensors of an automated garden with Raspberry.

This readme contains notes, thoughts, code snippets in no special order or relance.

# Setting up Raspberry for the first time

Format an SD card and install Raspberry Pi OS Lite (normal version with desktop is not necessary). 

https://www.raspberrypi.org/documentation/installation/installing-images/

After formatting, there will be two partitions: `boot` and `rootfs`. Place in `boot` two files:

- An empty file called `ssh` (this enables SSH access).
- A file called `wpa_supplicant.conf` with the following content:

```ini
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=ES

network={
 ssid="the_name_of_the_wifi"
 psk="the_password_of_the_wifi"
}
```

That setups the Wifi connection of the Raspberry.
Replace the name, password of the Wifi and the country by the appropriate ones.

Additional instructions to access Raspberry for the first time without monitor:

https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

## Login

Boot the Raspbbery and wait some minutes.

From your PC, connected to the same WIFI, run:

```sh
ssh pi@raspberrypi.local
```

Note, in some networks `raspberrypi.local` is not automatically detected. You need to find the exact IP. Normally, in the router admin page you can see the devices connected. You could find there the IP of the Raspberry. Then try ssh using the IP instead of `raspberrypi.local`.

The default password is "raspberry". After first login, change the password running `sudo passwd`.

## Upgrade packages to latest version

Run:

```sh
sudo apt update
sudo apt upgrade
sudo reboot
```

## Additional configuration

Run `sudo raspi-config` and then:

- Interfacing options / I2C / Enable
- Interfacing options / SPI / Enable
- Localisation options / Locale
- Localisation options / Timezone

## Install additional packages

```sh
sudo apt-get install python3-pip python3-smbus python3-dev i2c-tools
sudo apt-get install libpq5 # to access Postgre
```

## Install Pyhton dependencies

```sh
pip3 install seeed-python-si114x
pip3 install bme680
pip3 install scd30_i2c
pip3 install adafruit-circuitpython-mcp3xxx
pip3 install psycopg2-binary # to access Postgre
```

# Installing the application

- Create directory `/boot/future-foods`.
- Copy `code/main.py` to `/boot/future-foods/main.py`.
- Copy `install/future-foods-sensor.service` to `/etc/systemd/system/future-foods-sensor.service`.
- Run:

```sh
sudo systemctl daemon-reload
sudo systemctl enable future-foods-sensor # Start the service automatically on boot
```

# Post installation

It is very much recommended to enable Overlay FS to prevent damaging the SD card due to continuos writes or corrupting the file system due to sudden loss of power.

Run `sudo raspi-config` and activate: Performance / Overlay FS.

From now on any change in the root file system will be lost after reboot. To make permanent changes, for example to upgrade packages, you need to disable the Overlay FS first.

Changes inside `/boot` are permanent across reboots, that's why the code is installed there. Then it possible to upgrade it without disabling the Overlay FS.

You could also choose to make the `/boot` read-only when activating Overlay FS. It can be turn read-write at any moment (without disabling Overlay FS) with the command:

```sh
mount -o remount,rw /boot # set as read-write
mount -o remount,ro /boot # set as read-only
```

# Start stop the service

Run

```sh
sudo systemctl start future-foods-sensor # Start
sudo systemctl stop future-foods-sensor # Stop
systemctl status future-foods-sensor # Get status
systemctl status future-foods-sensor -n1000 # Get status and 1000 lines of logs
```

# Pinout

![Pinout Raspberry](media/pinout.png)

![Pinout Raspberry Zero](media/pinout-zero.png)

(License notes: these images have been extracted from external web sites, I am not the author)

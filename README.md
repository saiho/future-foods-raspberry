This is a very draft project for handling the sensors of an automated garden with Raspberry.

This readme contains miscellaneous notes, thoughts, code snippets, etc.


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
Replace the name and password of the Wifi and the country by the appropriate ones.

Additional instructions to access Raspberry for the first time without monitor:

https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

## Add an extra partition

After finishing the setup, the idea is to lock the two default partitions (`boot` and `rootfs`) setting them as readonly (see below, [Overlay FS](#overlay-fs)). To allow upgrading the application easily, a new partition is created. It will contain the application and some configuration files.

From Liux, shrink the `rootfs` partition. That can be done using several partition manager tools, or from the command line, using `resize2fs`. Then create a new EXT4 partition. Again, that can be done with a partition manager or the commands `parted` and `mkfs.ext4`.

## First boot, and login

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
- Localisation options / Timezone
- Localisation options / Locale


# Installing the application

## Install required packages

```sh
sudo apt-get install python3-pip python3-smbus python3-dev # Python
sudo apt-get install i2c-tools # sensors
sudo apt-get install libpq5 # Postgre
sudo apt-get install libwebp6 libtiff5 libopenexr23 libavformat58 libswscale5 liblapack3 libatlas3-base # camera
```

## Install Pyhton dependencies

```sh
# sensors
sudo pip3 install seeed-python-si114x
sudo pip3 install bme680
sudo pip3 install scd30_i2c
sudo pip3 install grove.py
sudo pip3 install gpiozero
sudo pip3 install adafruit-circuitpython-as7341

# to access Postgre
sudo pip3 install psycopg2-binary

# to capture images from usb camera
sudo pip3 install opencv-python-headless

# other, required
sudo pip3 install pyyaml
```

## Mount new partition

The idea is to have an entry in the `fstab` that will mount the new partition by default as read-only. When necessary, it could be remounted as read-write.

Get the PARTUUID of the new partition, running `blkid /dev/mmcblk0p3`.

Add to `/etc/fstab` the following line:

```
PARTUUID=ec3937c5-03  /app            ext4    ro,exec,nosuid,nodev,noatime,auto    0       2
```

## Install the code

- Create the directory of the app and give rights to the non-root user:

```sh
sudo mount -o rw /app # Mount as read-write
sudo mkdir /app/future-foods
sudo chown pi.pi /app/future-foods
```

- Copy `app/*` into `/app/future-foods`.
- Configure settings of `/app/future-foods/config.yml`.

Set as read-only:

```sh
chmod 600 config.yml # be sure that the configuration file is not readable by other users, since it contains sensitive information
sudo mount -o remount,ro /app # set as read-only
```

## Create a system service

- Copy `install/future-foods-sensor.service` to `/etc/systemd/system/future-foods-sensor.service`.
- Run:

```sh
sudo systemctl daemon-reload
sudo systemctl enable future-foods-sensor # Start the service automatically on boot
```


# Post installation

## Security

It is recommended that access to root account is protected with password. See: https://www.raspberrypi.org/documentation/configuration/security.md

To do that, still allowing the user `pi` to remount the partition of the application and start/stop the service, replace the content of `/etc/sudoers.d/010_pi-nopasswd` by:

```
pi ALL=(ALL) PASSWD: ALL
pi ALL=(root) NOPASSWD: /usr/bin/systemctl start future-foods-sensor
pi ALL=(root) NOPASSWD: /usr/bin/systemctl stop future-foods-sensor
pi ALL=(root) NOPASSWD: /usr/bin/systemctl restart future-foods-sensor
pi ALL=(root) NOPASSWD: /usr/bin/mount -o remount\,rw /app
pi ALL=(root) NOPASSWD: /usr/bin/mount -o remount\,ro /app
```

Note, the characters `,`, `:`, `=` and `\` must be escaped with `\` when they are part of the command arguments.

## Overlay FS

It is very much recommended to enable Overlay FS to prevent damaging the SD card due to continuos writes or corrupting the file system due to sudden loss of power.

Run `sudo raspi-config` and activate: Performance / Overlay FS.

From now on, any change in the root file system will be lost after reboot. To make permanent system changes, like installing or upgrading packages, you need to disable the Overlay FS first and reboot.

Changes inside `/app` are permanent across reboots. There is no need of disabling the Overlay FS, that's why the code is installed there.


## Starting and stoping the service on demand

```sh
sudo systemctl start future-foods-sensor # Start
sudo systemctl stop future-foods-sensor # Stop
systemctl status future-foods-sensor # Get status
systemctl status future-foods-sensor -n1000 # Get status and 1000 lines of logs
```

## Upgrading the code or updating settings

Every you need to modify the code or the settings, run:

```sh
sudo systemctl stop future-foods-sensor
sudo mount -o remount,rw /app
```

- Copy new `app/*` into `/app/future-foods`.
- Configure settings of `/app/future-foods/config.yml`.

```sh
sudo mount -o remount,ro /app
sudo systemctl start future-foods-sensor
```

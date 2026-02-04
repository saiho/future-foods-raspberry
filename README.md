This is a very draft project for handling the sensors of an automated garden with Raspberry.

This readme contains miscellaneous notes, thoughts, code snippets, etc.


# Setting up Raspberry for the first time

Install Raspberry Pi OS Lite (the normal version with desktop is not recommended) in a SD card using `rpi-imager`. Be sure to setup the Wi-Fi properly and enable ssh access.

https://www.raspberrypi.com/documentation/computers/getting-started.html#raspberry-pi-imager

Additional instructions to access Raspberry for the first time without using a screen:

https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi

## First boot, and login

Boot the Raspberry and wait some minutes. From a PC connected to the same Wi-Fi run:

```sh
ssh pi@raspberrypi.local
```

Use the password configured with `rpi-imager`.

Note, in some networks `raspberrypi.local` is not automatically detected. You need to find the exact IP. Normally, in the router admin page you can see the devices connected. You could find there the IP of the Raspberry. Then try ssh using the IP instead of `raspberrypi.local`.

To avoid entering the password everytime you connect, you can authorize the main PC to access the Raspberry running `ssh-copy-id zhome@zhome.local` from the PC.

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
sudo apt-get install webp fswebcam # camera
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

# other, required
sudo pip3 install pyyaml
```

## Partitions and OverlayFS

After finishing the setup, the idea is to lock the partitions `boot` and `rootfs`, setting them as read-only and activate the [OverlayFS](#enable-overlayfs). The OverlayFS allows to write in the protected partitions, keeping the changes only in memory but never writing them back in the SD card. This means that if the Raspberry is rebooted, all changes are lost. This prevents damaging the SD card due to frequent writes or corrupting the file system due to sudden loss of power.

To allow upgrading the application easily, we add an extra partition named `app` that will not be part of the OverlayFS. It will contain the application and some configuration files.


By default the `app` partition will be mounted as read-only. Everytime that becomes necessary to do changes, it has to be remounted as read-write, then save the data, and finally remount it as read-only. The reason to do this way is to flush changes as soon as possible and reduce the risk of file system corruption if the system crashes or it is shutted down suddenly.

### Add the app partition

Extract the SD Card from the Raspberry and open it in your main PC. Using Linux, shrink the `rootfs` partition, reducing it by 2 Gb. This can be done using several partition manager tools, or from the command line, using `resize2fs`. Note that the shrink should be done **after first boot**, otherwise the first boot could fail.

Then create a new EXT4 partition with the label `app`. Again, this can be done with a partition manager or the commands `parted` and `mkfs.ext4`.

### Mount the new partition

Put the SD Card back in the Raspberry, boot and connect.

Get the PARTUUID of the new partition, running `blkid /dev/mmcblk0p3`.

Add to `/etc/fstab` the following line:

```
PARTUUID=ec3937c5-03  /app            ext4    ro,exec,nosuid,nodev,noatime,auto    0       2
```

That entry will mount the new partition by default as read-only. When necessary, it could be remounted as read-write.

After modifying `fstab`, run `systemctl daemon-reload` and restart.

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

It is recommended to protect access to the root account with a password. See: https://www.raspberrypi.com/documentation/computers/configuration.html#secure-your-raspberry-pi

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

Note 2, be extra careful when editing `010_pi-nopasswd`. Any syntax error or wrong character will cause the file to be corrupted and it will not be possible to login as root.

## Enable OverlayFS

As explained in [Partitions and OverlayFS](#partitions-and-overlayfs), it is recommended to enable OverlayFS to protect the SD Card and reduce the risk of file system corruption.

Do some cleaning, like removing history files, logs or temporal files before enabling the OverlayFS.

Create the following file in `/etc/overlayroot.local.conf`:

```ini
#overlayroot="disabled"
overlayroot="tmpfs:recurse=0"
```

Note, the option "recurse=0" is to avoid that `/app` is added to the overlay, since we want it to be writable

Run in the Raspberry `sudo raspi-config` and activate: Performance / Overlay FS.

After rebooting, check with `mount` that the type of `/` is overlay but `/app` has not changed. If that is correct, the root partition will be "frozen" and the changes will be volatile.

You can find how much memory takes the OverlayFS by running `sudo du -hs /media/root-rw/overlay/*`.

### How to disable OverlayFS

There are two ways of making permanent system changes when OverlayFS is active:

1. Execute `mount -o remount,rw /media/root-ro`, make the changes under `/media/root-ro/`, and then `mount -o remount,ro /media/root-ro/`. If the files updated in `/media/root-ro/` were also modified in `/` and stay in memory, you won't see the changes made in `/media/root-ro/` propagated to `/` immediately.
2. Execute `overlayroot-chroot` and make the changes. If after exiting, the changes are not visible, run `mount -o remount /` to synchronize.

To disable OverlayFS, using one of the two methods described, uncomment the first line of `/etc/overlayroot.local.conf` and comment (with `#`) the second line. Then reboot.

To re-enable just revert the line comments and reboot.

## Starting and stoping the service on demand

```sh
sudo systemctl start future-foods-sensor # Start
sudo systemctl stop future-foods-sensor # Stop
systemctl status future-foods-sensor # Get status
systemctl status future-foods-sensor -n1000 # Get status and 1000 lines of logs
```

## Upgrading the code or updating settings

Every time you need to modify the code or the settings, run:

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

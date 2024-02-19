# pihole-oled

<p align="center"><img src="./res/pihole-oled-demo.gif"></p>

## Hardware

The OLED display is connected _via_ I2C with 4 wires: `SDA`, `SCL`, `3.3V` and
`GND`.

<p align="center"><img src="./res/pi-pinout.png"></p>

## Installation

:warning: This project requires a Raspberry Pi with
[Pi-hole](https://pi-hole.net/) installed, the I2C bus
enabled and Python 3. It uses the [luma.oled](https://github.com/rm-hull/luma.oled)
module which can drive a variety of displays.

### Software requirements

Install the following packages on debian/ubuntu:

```
sudo apt-get install python3-pip python3-setuptools python3-wheel python3-dev python3-humanize python3-psutil python3-requests zlib1g-dev libfreetype6-dev libjpeg-dev build-essential libopenjp2-7 i2c-tools libi2c-dev
```
### Project installation

Clone this project:

```
git clone https://github.com/LeDomme/pihole-oled
```

Install luma with pip3:

```
sudo -H pip3 install --upgrade luma.oled
```

Connect the OLED display and run the command below, you should see some
information on the display:

```
python3 pihole-oled.py
```

You can exit the script with <kbd>ctrl</kbd>+<kbd>c</kbd>.

### Systemd configuration

You can install a `systemd` service by copying the provided configuration file
using the command below.
But first you should change a few parameters in the ``` pihole-oled.service ``` file to your environment.

Change the user to your executing user
```
[Service]
Type=simple
User=pi
```
and change the working direcetory to yours
```
WorkingDirectory=/home/pi/pihole-oled
```

This service will automatically run the python script
mentioned in the previous section on boot:

```
sudo cp pihole-oled.service /etc/systemd/system/
```

The service runs as the user pihole so you will need to add that user to the i2c group.
Enable, then start the `pihole-oled.service`:

```
sudo systemctl enable pihole-oled.service
sudo systemctl start pihole-oled.service
```

## License

This project is released under the MIT License. See the bundled [LICENSE
file](./LICENSE) for details.

#!/usr/bin/python3

#base imports
import os
import platform
import time
from time import sleep
from datetime import datetime

#oled device imports
from luma.core.interface.serial import i2c
from luma.core.render import canvas
##
#Set oled display type here
#luma.oled supports ssd1306, ssd1309, ssd1322, ssd1322_nhd, ssd1325, ssd1327, ssd1331, ssd1351, sh1106
from luma.oled.device import ssd1306
##

#data and formatting
import humanize
import psutil
import requests

#PIL imports
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#API
##Set you API key here
api_token = "YOUR_API_KEY"
api_url = "http://localhost/admin/api.php?summaryRaw&auth="+api_token


#oled display setup
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)
font = ImageFont.truetype('SF_Pixelate.ttf', 10)
width = device.width
height = device.height

#os variables
#from systemd or default to eth0 and root
interface = os.getenv('PIHOLE_OLED_INTERFACE', 'eth0')
mount_point = os.getenv('PIHOLE_OLED_MOUNT_POINT', '/')
hostname = platform.node()

#Reduce contrast to prevent burn in
#Adjust as needed
device.contrast(5)

#begin loop
device.clear()

#Wait X Seconds per display
sleep = 2

try:
    elapsed_seconds = 0
    while True:
        with canvas(device) as draw:
            draw.rectangle(
                (0, 0, width, height), 
                outline=0, 
                fill=0
            )
            if elapsed_seconds == 10:
                elapsed_seconds = 0
            if elapsed_seconds >= 5:
                addr = psutil.net_if_addrs()[interface][0]
                draw.text(
                    (0, 0),
                    "%s" % hostname.ljust(8) + "%s" % addr.address.rjust(15),
                    font=font,
                    fill=255
                )
                uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
                draw.text(
                    (0, 12),
                    "Uptime: %s" % humanize.naturaldelta(uptime),
                    font=font,
                    fill=255
                )
                draw.text(
                    (0, 22),
                    "     %.1f %.1f %.1f" % os.getloadavg(),
                    font=font,
                    fill=255
                )
                cpu = int(psutil.cpu_percent(percpu=False))
                draw.text(
                    (0, 34), 
                    "CPU", 
                    font=font, 
                    fill=255
                )
                draw.rectangle(
                    (26, 34, 126, 34 + 6), 
                    outline=255, 
                    fill=0
                )
                draw.rectangle(
                    (26, 34, 26 + cpu, 34 + 6), 
                    outline=255, 
                    fill=255
                )
                mem = int(psutil.virtual_memory().percent)
                draw.text(
                    (0, 44), 
                    "RAM", 
                    font=font, 
                    fill=255
                )
                draw.rectangle(
                    (26, 44, 126, 44 + 6), 
                    outline=255, 
                    fill=0
                )
                draw.rectangle(
                    (26, 44, 26 + cpu, 44 + 6), 
                    outline=255, 
                    fill=255
                )
                disk = int(psutil.disk_usage(mount_point).percent)
                draw.text(
                    (0, 54), 
                    "Disk", 
                    font=font, 
                    fill=255
                )
                draw.rectangle(
                    (26, 54, 126, 54 + 6), 
                    outline=255, 
                    fill=0
                )
                draw.rectangle(
                    (26, 54, 26 + disk, 54 + 6), 
                    outline=255, 
                    fill=255
                )
            else:
                try:
                    req = requests.get(api_url)
                    data = req.json()
                    draw.text(
                        (0, 0),
                        "%s" % hostname.ljust(8) +
                        "%s" % data["status"].rjust(13),
                        font=font,
                        fill=255
                    )
                    draw.line(
                        (0, 12, width, 12), 
                        fill=255
                    )
                    draw.text(
                        (0, 22),
                        "Blocked: %d (%d%%)" % (
                            data["ads_blocked_today"],
                            data["ads_percentage_today"]
                        ),
                        font=font,
                        fill=255
                    )
                    draw.text(
                        (0, 32),
                        "Queries: %d" % data["dns_queries_today"],
                        font=font,
                        fill=255
                    )
                    draw.line(
                        (0, 50, width, 50), 
                        fill=255
                    )
                    draw.text(
                        (0, 54),
                        "Blocklist: %d" % data["domains_being_blocked"],
                        font=font,
                        fill=255
                    )
                except:
                    draw.text(
                        (0, 0), 
                        "ERROR!", 
                        font=font, 
                        fill=255
                    )
        time.sleep(sleep)
        elapsed_seconds += 1
except (KeyboardInterrupt, SystemExit):
    device.hide()
    print("Exiting...")

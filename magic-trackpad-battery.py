#!/usr/bin/env python3
import fcntl
import os
import json
import sys

REPORT_ID = 0x90
REPORT_SIZE = 3
HIDIOCGINPUT = 0xC003480A 

def find_device():
    base = "/sys/class/hidraw"
    try:
        for node in os.listdir(base):
            uevent = f"{base}/{node}/device/uevent"
            if os.path.exists(uevent):
                with open(uevent, "r") as f:
                    if "DRIVER=magicmouse" in f.read():
                        return f"/dev/{node}"
    except Exception:
        return None
    return None

def get_data():
    device = find_device()
    if not device:
        return None

    try:
        fd = os.open(device, os.O_RDWR)
        
        buf = bytearray([REPORT_ID, 0, 0])
        fcntl.ioctl(fd, HIDIOCGINPUT, buf)
        os.close(fd)

        # buf[1] -> (Bit 0x02 indicates if it's charging)
        # buf[2] -> Capacity (0-100)
        return int(buf[2]), bool(buf[1] & 0x02)
    except Exception:
        return None

def main():
    result = get_data()
    if not result:
        sys.exit(0)

    percent, charging = result

    css_class = "fine"
    if percent <= 20: css_class = "warning"
    if percent <= 10: css_class = "critical"

    icon = "󱐋󰟸" if charging else "󰟸"

    output = {
        "text": f"{icon} {percent}%",
        "class": css_class,
        "percentage": percent,
        "tooltip": "Batería Magic Trackpad"
    }
    
    print(json.dumps(output))

if __name__ == "__main__":
    main()
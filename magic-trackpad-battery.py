#!/usr/bin/env python3
import fcntl
import os
import json
import sys
import subprocess

# HID Report Configuration
REPORT_ID = 0x90
HIDIOCGINPUT = 0xC003480A 

def get_battery_upower():
    """
    Searches for the Magic Trackpad via upower.
    Useful when the device is connected via USB or HIDRAW does not respond.
    """
    try:
        devices = subprocess.check_output(["upower", "-e"], text=True).splitlines()
        
        for path in devices:
            info = subprocess.check_output(["upower", "-i", path], text=True)
            if "Magic Trackpad" in info:
                lines = [line.strip() for line in info.splitlines()]
                data = {}
                for line in lines:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        data[key.strip()] = value.strip()
                
                percent = int(data.get("percentage", "0").replace("%", ""))
                state = data.get("state", False)
                return percent, state
    except Exception:
        return None
    return None

def get_data():
    base = "/sys/class/hidraw"
    if not os.path.exists(base): return None

    try:
        for node in os.listdir(base):
            uevent_path = f"{base}/{node}/device/uevent"
            if not os.path.exists(uevent_path): continue
            
            with open(uevent_path, "r") as f:
                content = f.read()
                if "DRIVER=magicmouse" in content:
                    
                    # Case 1: USB Connection
                    if "HID_PHYS=usb" in content:
                        return get_battery_upower()
                    
                    # Case 2: Bluetooth Connection
                    device = f"/dev/{node}"
                    try:
                        fd = os.open(device, os.O_RDWR)
                        buf = bytearray([REPORT_ID, 0, 0])
                        fcntl.ioctl(fd, HIDIOCGINPUT, buf)
                        os.close(fd)
                        
                        percent = int(buf[2])
                        charging = bool(buf[1] & 0x02)
                        return percent, charging
                    except:
                        return get_battery_upower()
    except Exception:
        return None
    return None

def main():
    result = get_data()
    if not result:
        sys.exit(0)
    
    percent, charging = result
    
    css_class = "fine"
    if percent <= 35: css_class = "warning"
    if percent <= 20: css_class = "critical"
    
    icon = "󱐋󰟸" if charging else "󰟸"

    output = {
        "text": f"{icon} {percent}%",
        "class": css_class,
        "percentage": percent,
        "tooltip": f'Apple Magic Trackpad Battery: {percent}% {"(Charging)" if charging else ""}'
    }
    
    print(json.dumps(output))

if __name__ == "__main__":
    main()
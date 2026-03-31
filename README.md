# apple-magic-trackpad-battery-percent-python
Python script  to show the Magic Trackpad battery percentage on Waybar

![Waybar Magic Trackpad Demo](demo.png)

Since the hid_magicmouse driver often fails to report battery levels to upower when connected via Bluetooth, this script uses ioctl to query the hardware directly (using the 0x90 report ID)

**Note:** In some cases, when the Apple Magic Trackpad is charging directly on the same device, the connection type changes from Bluetooth to USB. Therefore, the script uses an alternative path to obtain battery information in these situations.

Requirements:
- Python 3.7 or higher
- Nerd Fonts (for icons, or change them to whatever you want)

1. Set Permissions (udev rule)
First, we need permission to read the hardware node without being root. This rule assigns the device to the input group
Run this command:

```bash
echo 'SUBSYSTEM=="hidraw", DRIVERS=="magicmouse", MODE="0660", GROUP="input"' | sudo tee /etc/udev/rules.d/99-magictrackpad.rules && sudo udevadm control --reload-rules && sudo udevadm trigger
```
2.  Python Script

Clone this repo and give it execute permissions:

```bash
chmod +x magic-trackpad-battery.py
```

move it to your Waybar scripts directory (or anywhere you like, just update the path in the Waybar config)

3. Waybar module

```json
"custom/magic-trackpad-battery": {
    "exec": "$HOME/.config/waybar/scripts/magic-trackpad-battery.py",
    "return-type": "json",
    "interval": 60,
    "format": "{}",
    "tooltip": true
},
```


4. CSS Style

You can add colors based on the battery level

```css
#custom-magic-trackpad-battery.warning {
    color: #fab387;
}
#custom-magic-trackpad-battery.critical {
    color: #f38ba8;
}
```
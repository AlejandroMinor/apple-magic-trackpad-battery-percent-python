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

2. Add your user to the input group

Some distributions (notably vanilla Arch Linux) do not add users to the `input` group by default. If that's your case, add yourself manually:

```bash
sudo usermod -aG input $USER
```

You must fully log out and log back in (or reboot) for this to take effect — opening a new terminal is not enough. To verify:

```bash
groups
```

`input` should appear in the list.

> **A note on security:** Adding your user to the `input` group is the simplest approach and works out of the box, but it does grant broader access to input devices than strictly necessary. If you'd prefer a more targeted setup, there's a [safer alternative](#alternative-dedicated-group-for-stricter-permissions) at the end of this document that limits access to the trackpad only.

3.  Python Script

Clone this repo and give it execute permissions:

```bash
chmod +x magic-trackpad-battery.py
```

move it to your Waybar scripts directory (or anywhere you like, just update the path in the Waybar config)

4. Waybar module

```json
"custom/magic-trackpad-battery": {
    "exec": "$HOME/.config/waybar/scripts/magic-trackpad-battery.py",
    "return-type": "json",
    "interval": 60,
    "format": "{}",
    "tooltip": true
},
```


5. CSS Style

You can add colors based on the battery level

```css
#custom-magic-trackpad-battery.warning {
    color: #fab387;
}
#custom-magic-trackpad-battery.critical {
    color: #f38ba8;
}
```

## Alternative: dedicated group (for stricter permissions)

If you prefer not to add your user to the system-wide `input` group, you can create a dedicated group that grants access only to the Magic Trackpad:

```bash
sudo groupadd -f magictrackpad
sudo usermod -aG magictrackpad $USER
sudo tee /etc/udev/rules.d/99-magictrackpad.rules > /dev/null <<'EOF'
SUBSYSTEM=="hidraw", DRIVERS=="magicmouse", MODE="0660", GROUP="magictrackpad"
EOF
sudo udevadm control --reload-rules && sudo udevadm trigger
```

You still need to log out and back in (or reboot) for the group membership to take effect. With this approach your user only gains access to the trackpad device, without any additional permissions over other input devices.
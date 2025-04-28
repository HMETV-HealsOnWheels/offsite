# Heals on Wheels – Offsite System

This repository contains the **offsite components** of the Heals on Wheels project, including the graphical interface used to control the autonomous medical cart. While the onboard system runs on the Raspberry Pi and Arduino, the offsite system runs on a laptop and sends commands over TCP. In the future, this system can be extended to include a web-based or mobile interface, allowing for more flexible and user-friendly interaction with the cart across different devices.

---

## What is the Offsite System?

In this project, "offsite" refers to any computing that does **not run on the physical cart** (the Raspberry Pi or Arduino). Instead, it includes tools and interfaces used by hospital staff or developers to interact with the cart remotely.

The offsite system allows users to:
- Send movement commands to the robot
- Trigger an emergency stop
- Select predefined destinations
- Monitor robot connection and movement logs

---

## GUIs Available

1. `test_gui.py`
A simple tkinter-based Python GUI used for testing cart movement.
- Send basic commands (forward, backward, left, right, stop)
- Set manual durations for moves
- Emergency stop functionality
**Used during initial development and system testing.**

2. `client_gui.py`
The **final GUI** used for deployment at Cook Children’s Hospital demonstration.
- Modernized, user-friendly interface
- Pre-programmed destination paths (e.g., ICU 1, ICU 2, Room 1, Room 2)
- Automatic connection checking to the Raspberry Pi
- Emergency stop button
- Operation log tracking
- Responsive design for different screen sizes
**This was the official GUI showcased on demo day.**

### How It Connects

Both GUIs communicate with the TCP server defined in the **Onboard Repository** [`server.py`](https://github.com/HMETV-HealsOnWheels/onboard/blob/main/server.py).  
It sends string-based commands over port **5001** to the Raspberry Pi’s IP address.

---

## How to Use

1. Connect your laptop to the same network as the Raspberry Pi, in our case it was Skynet Wifi.
2. Confirm the Raspberry Pi's IP using an IP scanner
3. Update the `TCP_IP` value in `test_gui.py` or `client_gui.py` if needed
4. Run the GUI:

```bash
python3 client_gui.py
```
```bash
python3 test_gui.py
```

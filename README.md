# Heals on Wheels – Offsite System

This repository contains the **offsite components** of the Heals on Wheels project, including the graphical interface used to control the autonomous medical cart. While the onboard system runs on the Raspberry Pi and Arduino, the offsite system runs on a laptop and sends commands over TCP. In the future, this system can be extended to include a web-based or mobile interface, allowing for more flexible and user-friendly interaction with the cart across different devices.

---

## What is the Offsite System?

In this project, "offsite" refers to any computing that does **not run on the physical cart** (the Raspberry Pi or Arduino). Instead, it includes tools and interfaces used by hospital staff or developers to interact with the cart remotely.

The main component in this repository is a **desktop GUI application** that allows users to send movement commands to the robot over the network.

---

## GUI: `cart_controller_gui.py`
This is a simple `tkinter`-based Python application that sends commands to the onboard server running

- Send individual commands (like `forward`, `stop`, etc.)
- Specify a duration for movement
- Trigger an emergency stop

### How It Connects

This GUI communicates with the TCP server defined in the **Onboard Repository** [`server.py`](https://github.com/HMETV-HealsOnWheels/onboard/blob/main/server.py).  
It sends string-based commands over port **5001** to the Raspberry Pi’s IP address.

---

## How to Use

1. Ensure your laptop is on **Skynet WiFi**
2. Confirm the Raspberry Pi's IP using an IP scanner
3. Update the `TCP_IP` value in `cart_controller_gui.py` if needed
4. Run the GUI:

```bash
python3 cart_controller_gui.py
```


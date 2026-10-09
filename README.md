# Drone SITL — Takeoff and Arm

A Python script that connects to an ArduPilot SITL drone, arms the motors, takes off to a target altitude, hovers briefly, and lands — all autonomously via MAVLink. This is the second step in drone autonomy: commanding the drone to fly under script control.

## What It Does

- Connects to the drone via MAVLink (UDP) and waits for a heartbeat
- Switches the flight controller to **GUIDED** mode
- Arms the motors and waits for confirmation
- Commands a takeoff to **10 metres**
- Monitors real altitude via `GLOBAL_POSITION_INT` until the target is reached
- Hovers for 5 seconds, then switches to **LAND** mode

## Prerequisites

- **ArduPilot SITL** — built and ready to run via `sim_vehicle.py`
- **Python 3** with **pymavlink** installed
- A Linux machine (tested on Ubuntu 24.04, Raspberry Pi 5 ARM64)

### Install pymavlink (if not already installed)

```bash
pip install pymavlink
```

## How to Run

### Step 1: Launch SITL

Open a terminal and start the ArduPilot simulator:

```bash
sim_vehicle.py -v ArduCopter --console --map
```

Wait until you see `APM: EKF2 IMU0 is using GPS` — this means the simulated drone has a GPS lock and is ready.

> **Tip:** You can set a custom home location with the `-l` flag:
> ```bash
> sim_vehicle.py -v ArduCopter --console --map -l 17.249028,78.557111,540,0
> ```
> Format: `lat,lon,alt,heading`

### Step 2: Run the Takeoff Script

In a **separate terminal**, run:

```bash
python3 takeoff_and_arm.py
```

### Expected Output

```
Connecting...
Connected to system 1
Setting GUIDED mode...
Arming...
Armed!
Taking off...
Altitude: 0.1 m
Altitude: 1.3 m
Altitude: 3.7 m
Altitude: 6.2 m
Altitude: 8.9 m
Altitude: 9.6 m
Reached target altitude.
Hovering for 5 seconds...
Landing...
Land command sent. Watch it descend.
```

The drone will climb to ~10 m, hover, and then descend automatically.

## How It Works

| Step | Command / Method | Purpose |
|------|-----------------|---------|
| Connect | `mavutil.mavlink_connection('udpin:127.0.0.1:14550')` | Open MAVLink UDP link |
| Heartbeat | `master.wait_heartbeat()` | Confirm the link is alive |
| GUIDED mode | `master.set_mode(master.mode_mapping()['GUIDED'])` | Enable script-controlled flight |
| Arm | `MAV_CMD_COMPONENT_ARM_DISARM` (param1 = 1) | Spin up the motors |
| Takeoff | `MAV_CMD_NAV_TAKEOFF` (param7 = altitude) | Climb to target altitude |
| Monitor | `GLOBAL_POSITION_INT.relative_alt / 1000` | Poll real altitude (mm → m) |
| Land | Set mode to `LAND` | Autonomous descent and disarm |

## Connection Details

| Parameter         | Value                        |
|-------------------|------------------------------|
| Protocol          | MAVLink over UDP             |
| Connection String | `udpin:127.0.0.1:14550`      |
| Default SITL Port | 14550 (14551 if 14550 is busy) |

For **real hardware** (e.g., Pixhawk via USB), change the connection string to:

```python
master = mavutil.mavlink_connection('/dev/ttyACM0', baud=115200)
```

## Safety Note

**SITL success does not guarantee hardware safety.** On a real drone: bench-test with **props removed** first, verify arming and mode response, then fly conservatively at low altitude with the ability to take manual RC control.

## Project Context

This is part of a larger drone autonomy project built on ArduPilot + pymavlink, progressing step-by-step from basic telemetry to autonomous missions and multi-drone formations.

from pymavlink import mavutil
import time

# 1. Connect and wait for the vehicle
print("Connecting...")
master = mavutil.mavlink_connection('udpin:127.0.0.1:14550')
master.wait_heartbeat()
print(f"Connected to system {master.target_system}")

# 2. Switch to GUIDED mode
print("Setting GUIDED mode...")
master.set_mode(master.mode_mapping()['GUIDED'])
time.sleep(2)

# 3. Arm the motors
print("Arming...")
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,        # confirmation
    1,        # 1 = arm
    0, 0, 0, 0, 0, 0)
master.motors_armed_wait()   # blocks until actually armed
print("Armed!")

# 4. Take off to 10 metres
print("Taking off...")
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0,
    0, 0, 0, 0, 0, 0,
    10)       # target altitude in metres

# 5. Watch it climb
while True:
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    alt = msg.relative_alt / 1000.0
    print(f"Altitude: {alt:.1f} m")
    if alt >= 9.5:            # close enough to 10
        print("Reached target altitude.")
        break
    time.sleep(0.5)

# 6. Hover a bit, then land
print("Hovering for 5 seconds...")
time.sleep(5)

print("Landing...")
master.set_mode(master.mode_mapping()['LAND'])
print("Land command sent. Watch it descend.")
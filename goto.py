from dronekit import connect,VehicleMode,LocationGlobalRelative,LocationGlobal
import time
vehicle=connect("udp:127.0.0.1:14550",wait_ready=True)

vehicle.mode = VehicleMode("GUIDED")

# Set the target location in global-relative frame
a_location = LocationGlobalRelative(-34.364114, 149.166022, 30)
vehicle.simple_goto(a_location)

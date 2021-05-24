from dronekit import connect,VehicleMode,LocationGlobalRelative,LocationGlobal
import time
from pymavlink import mavutil
import pygame
vehicle=connect("udp:127.0.0.1:14550",wait_ready=True)

gnd_speed = 5

pygame.init()
pygame.display.set_mode((150,150))

def arm_and_takeoff(altitude):
    print("basic checkup")
    while not vehicle.is_armable:
        print("waiting to initialize")
        time.sleep(1)
    print("arming motors")
    vehicle.mode=VehicleMode("GUIDED")
    vehicle.armed=True

    while not vehicle.armed:
        print("waiting to be armed")
        time.sleep(1)
    print(vehicle.home_location)
    print("taking off")
    vehicle.simple_takeoff(altitude)

    while True:
        print("altitude: {val}".format(val=vehicle.location.global_relative_frame.alt))
        
        if vehicle.location.global_relative_frame.alt>=altitude*0.95:
            print("target altitude reached")
            break
        time.sleep(1)

def send_ned_velocity(vehicle,vx,vy,vz):
    msg=vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0,0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0,0,0,
        vx,vy,vz,
        0,0,0,
        0,0)
    vehicle.send_mavlink(msg)
    vehicle.flush()

arm_and_takeoff(10)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_w:
            send_ned_velocity(vehicle,gnd_speed,0,0,)
           elif event.key == pygame.K_s:
              send_ned_velocity(vehicle,-gnd_speed,0,0)
           elif event.key == pygame.K_a:
              send_ned_velocity(vehicle,0,-gnd_speed,0)
           elif event.key == pygame.K_d:
              send_ned_velocity(vehicle,0,gnd_speed,0)   

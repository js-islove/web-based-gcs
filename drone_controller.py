# drone control module

import time
import logging
from dronekit import connect , VehicleMode
from pymavlink import mavutil


class DroneController:
    def __init__(self , connection_string , takeoff_alt = 10 , rtl_alt = 15):
        
        try:
             self.vehicle = connect(connection_string , baud= 57600 , wait_ready=True)
             logging.info(f'drone connected to {connection_string}')
        except Exception as e:
            logging.error(f'Failed to connect the drone {e}')
            
        
        self.takeoff_alt = takeoff_alt
        self.rtl_alt = rtl_alt
        self.state = "disarmed"
        
    def get_telemetry(self):
        if not self.vehicle:
            logging.error("No drone connection found")
            
        try :
            
            return{
                'altitude' : self.vehicle.location.global_relative_frame.alt,
                'latitude' : self.vehicle.location.global_relative_frame.lat,
                'longitude' : self.vehicle.location.global_relative_frame.lon,
                'speed' : self.vehicle.battery.voltage,
                'state' : self.state
                
            }
        except Exception as e:
            logging.error(f'Error getting telemetry{e}')
    
    
    def takeoff(self):
        if not self.vehicle:
            logging.error("error taking off")
            
            return
        
        try:
            self.vehicle.mode = VehicleMode("GUIDED")
            self.vehicle.armed = True
            while not self.vehicle.armed:
                time.sleep(1)
            self.vehicle.simple_takeoff(self.takeoff_alt)
            logging.info("taking off")
            while self.vehicle.location.global_relative_frame.alt < self.takeoff_alt * 0.95:
               time.sleep(1)
            logging.info("takeoff complete")
            self.state = "AIRBORNE"
        except Exception as e:
            logging.info(f'error during takeoff{e}')
            
    
    def land(self):
        if not self.vehicle:
            logging.error("No drone connection")
            
            return
        try:
            self.vehicle.mode = VehicleMode("LAND")
            logging.info('landing..')
            self.state = "LANDING"
        except Exception as e:
            logging.error(f'error during landing{e}')
            
    def return_home(self):
        
        if not self.vehicle:
            logging.error("No drone connection.")
            return
        
        try:
            self.vehicle.mode = VehicleMode("RTL")
            logging.info("Returning to launch")
            self.state = "RETURNING"
        except Exception as e:
            logging.error(f'Error during return home: {e}')
            
    def move(self, vx, vy, vz):
        
        if not self.vehicle:
            logging.error("No drone connection.")
            return
        
        try:
            msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
                0, 0, 0, mavutil.mavlink.MAV_FRAME_BODY_NED, 0b0000111111000111,
                0, 0, 0, vx, vy, vz, 0, 0, 0, 0, 0
            )
            self.vehicle.send_mavlink(msg)
            self.vehicle.flush()
        except Exception as e:
            logging.error(f'Error moving drone: {e}')
    
    def stop(self):
        
        self.move(0, 0, 0)
        logging.info("Drone stopped")
    
    def close(self):
        
        if not self.vehicle:
            logging.error("No drone connection.")
            return
        
        try:
            self.vehicle.close()
            logging.info("Drone disconnected")
        except Exception as e:
            logging.error(f'Error closing drone connection: {e}')

            

               
        
        
       
        

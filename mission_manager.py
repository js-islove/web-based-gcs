# waypoint mission manager
import logging
from dronekit import Command , VehicleMode
from pymavlink import mavutil
from drone_controller import DroneController
# i have found a issue just above this line , i will lock after it it is related to self.drone
class MissionManager:
    def __init__(self , drone):
        self.drone = DroneController()
        
    def upload_mission(self , waypoints):
        cmds = self.drone.vehicle.commands
        cmds.clear()
        
        for wp in waypoints:
            cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                             mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0,
                             float(wp['latitude']), float(wp['longitude']), float(wp['altitude'])))
            cmds.upload()
            logging.info("mission uploaded successfully")
            
    def start_mission(self):
        if self.drone.vehicle.mode.name != "AUTO":
            self.drone.vehicle.mode = VehicleMode("AUTO")
        logging.info("Mission started..")
        
    def pause_mission(self):
        self.drone.vehicle.mode = VehicleMode("GUIDED")
        logging.info("mission  paused")
        
    def cancel_mission(self):
        cmds = self.drone.vehicle.commands
        cmds.clear()
        cmds.upload()
        self.drone.vehicle.mode = VehicleMode("GUIDED")
        logging.info("Mission canceled and waypoints cleared.")
        
        
            
        
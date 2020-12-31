# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import airsim #pip install airsim
import time
import os
import psutil
import pprint
import platform
import threading
import numpy as np
import matplotlib.pyplot as plt

MAZE = 0
AIRSIMNH = 1
BLOCKS = 2
CITY = 3
COASTLINE = 4
LANDSCAPE = 5
SOCCER = 6

MANUAL = 0
AUTO = 1

#################################################################################
## =============================== CAR METHODS =============================== ##
#################################################################################

clientCM = None

class CarMethods(object):
    
    ## ======================= SETTERS AND GETTERS ===========================         
        
    def getClient(self):
        global clientCM
        return clientCM
    
    def hasSimulationStarted(self):
        global controlAirSim
        return not(controlAirSim)
        
    ## ============================= METHODS ================================= 
    
    def printHomePosition(self):
        print(self.getClient().getHomeGeoPoint())
        
    def getHomePositionAltitude(self):
        return self.getClient().getHomeGeoPoint().altitude
    
    def getHomePositionLatitude(self):
        return self.getClient().getHomeGeoPoint().latitude
    
    def getHomePositionLongitude(self):
        return self.getClient().getHomeGeoPoint().longitude
    
    def getSpeed(self):
        # In m/s
        return self.getClient().getCarState('Car1').speed
    
    def getCarPose(self):
        return self.getClient().simGetVehiclePose("Car1") 
    
    def getEstimatedPos(self):
        return self.getClient().getCarState('Car1').kinematics_estimated.position
    
    def getEstimatedOrientation(self):
        return self.getClient().getCarState('Car1').kinematics_estimated.orientation
    
    def getIMU_Data(self):
        return self.getClient().getImuData('IMU','Car1')
    
    def getIMU_AngularVelocity(self):
        return self.getClient().getImuData('IMU','Car1').angular_velocity
    
    def getIMU_LinearAcceleration(self):
        return self.getClient().getImuData('IMU','Car1').linear_acceleration
    
    def getIMU_Orientation(self):
        return self.getClient().getImuData('IMU','Car1').orientation
    
    def getSONAR_Data(self):
        return self.getClient().getDistanceSensorData('Distance','Car1').distance
    
    def getLIDAR_Data(self):
        return self.getClient().getLidarData('LIDAR','Car1')
    
    def getLIDAR_PointCloud(self):
        return self.getClient().getLidarData('LIDAR','Car1').point_cloud
    
    def getGPS_Data(self):
        return self.getClient().getGpsData('GPS','Car1')
        
    def getCameraShoot(self):
        images = self.getClient().simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene,False,False)])
        
        for image in images:
            #print("Type %d, size %d" % (image.image_type, len(image.image_data_uint8)))
            img1d = np.fromstring(image.image_data_uint8, dtype=np.uint8) # get numpy array
            img_rgb = img1d.reshape(image.height, image.width, 3) # reshape array to 3 channel image array H X W X 3
            
        return img_rgb
        
#################################################################################        
## ============================ TOURNAMENT METHODS =========================== ##        
#################################################################################

from files.TeamsMethods import TeamsMethods
team = TeamsMethods()
client = None
car_controls = None
controlAirSim = True
manualMode = False

position_map = []
speed_map = []
throttle_map = []
brake_map = []
steering_map = []
        

class Tournament():

    ## =========================== CONSTRUCTORS ==============================         
    
    def __init__(self,team,environ,operationMode):
        self.__setTeam(team)
        self.__setOperationMode(operationMode)
        self.run(environ)
    
    ## ======================= SETTERS AND GETTERS ===========================         
    
    def __setTeam(self,t):
        global team
        team = t
        
    def __setOperationMode(self,m):
        global mode, manualMode
        mode = m
        if mode == MANUAL:
            manualMode = True
        else:
            manualMode = False

    def __setClient(self,c):
        global client
        client = c
        
    def __setClientCM(self,c):
        global clientCM
        clientCM = c

    def __setCarControls(self,cc):
        global car_controls
        car_controls = cc
        
    def getTeam(self):
        global team
        return team
    
    def getMode(self):
        global mode
        return mode
        
    def getClient(self):
        global client
        return client
    
    def getClientCM(self):
        global clientCM
        return clientCM

    def getCarControls(self):
        global car_controls
        return car_controls        
    
    ## ============================= METHODS ================================= 
    
    def __airSimClientConnection(self):
        global client, clientCM, manualMode
        
        self.__setClient(airsim.CarClient(timeout_value = 10000))
        self.__setClientCM(airsim.CarClient())
        self.getClient().confirmConnection()
        
        #print("Do you want to activate the manual mode? [y/n]")
        if manualMode == False:
            self.getClient().enableApiControl(True)
            print('Automatic mode activated\n')
        else: 
            print('Manual mode activated\n')

        self.__setCarControls(airsim.CarControls())
        time.sleep(2)
        
    def __setVehiclePose(self,pose):
        self.getClient().simSetVehiclePose(pose, True, 'Car1')
        
    def __getVehiclePose(self):
        return self.getClient().simGetVehiclePose("Car1")    
        
    def __printMessage(self, message):
        self.getClient().simPrintLogMessage(message)
        
    def __collisionPrint(self, collision_info):
        print("Collision at pos %s, normal %s, impact pt %s, penetration %f, name %s, obj id %d" % (
            pprint.pformat(collision_info.position), 
            pprint.pformat(collision_info.normal), 
            pprint.pformat(collision_info.impact_point), 
            collision_info.penetration_depth, collision_info.object_name, collision_info.object_id))
    
    def __updateCarControls(self):      
        throttle = self.getTeam().getThrottle()
        self.getCarControls().throttle = throttle
        
        if(throttle >= 0.0): ## Activate Automatic gear
            self.getCarControls().is_manual_gear = False; # change back gear to auto
            self.getCarControls().manual_gear = 0 
        else: ## Activate reverse Gear
            self.getCarControls().is_manual_gear = True;
            self.getCarControls().manual_gear = -1
            
        self.getCarControls().brake = self.getTeam().getBrake()
        self.getCarControls().steering = self.getTeam().getSteering()
        self.getClient().setCarControls(self.getCarControls())
        
    def __updateReport(self):
        global position_map, speed_map, throttle_map, brake_map, steering_map
        position_map.append(self.getClient().simGetVehiclePose("Car1").position)    
        speed_map.append(self.getClient().getCarState('Car1').speed)
        throttle_map.append(self.getTeam().getThrottle())
        brake_map.append(self.getTeam().getBrake())
        steering_map.append(self.getTeam().getSteering())
        
    def __clearVariables(self):
        global team, client, car_controls, controlAirSim, manualMode, position_map, speed_map, throttle_map, brake_map, steering_map, clientCM
        team = TeamsMethods()
        client = None
        clientCM = None
        car_controls = None
        controlAirSim = True
        manualMode = False

        position_map.clear()
        speed_map.clear()
        throttle_map.clear()
        brake_map.clear()
        steering_map.clear()

    def run(self,environ):        
        ## Variable that control the Unreal launch
        global position_map, speed_map, throttle_map, brake_map, steering_map
        global controlAirSim, manualMode
        global clientCM
        controlAirSim = True
        
        while(controlAirSim):
            time.sleep(2)
            
            if(environ+".exe" in (p.name() for p in psutil.process_iter())):
                time.sleep(5)
                
                ## Connect to the AirSim simulator 
                self.__airSimClientConnection()
                
                ## Setting Day and Hour of the Environment
                #self.getClient().simSetTimeOfDay(True,'2020-07-10 14:00:00')
                
                ## Enable Wheather in Scene: Rain, RoadWetness, Snow, RoadSnow
                ## MapleLeaf, RoadLeaf, Dust and Fog from 0 to 1.
                #self.getClient().simEnableWeather(True)
                #self.getClient().simSetWeatherParameter(airsim.WeatherParameter.Enabled, 1.0);
                #self.getClient().simSetWeatherParameter(airsim.WeatherParameter.Rain, 1.0);
                #self.getClient().simSetWeatherParameter(airsim.WeatherParameter.Roadwetness, 1.0);
                #self.getClient().simSetWeatherParameter(airsim.WeatherParameter.Snow, 1.0);
                #self.getClient().simSetWeatherParameter(airsim.WeatherParameter.RoadSnow, 1.0);
                #self.getClient().simSetWeatherParameter(airsim.WeatherParameter.MapleLeaf, 1.0);
                #self.getClient().simSetWeatherParameter(airsim.WeatherParameter.RoadLeaf, 1.0);
                #self.getClient().simSetWeatherParameter(airsim.WeatherParameter.Dust, 1.0);
                #self.getClient().simSetWeatherParameter(airsim.WeatherParameter.Fog, 1.0);
            
                ## Setting Vehicle Initial Pose:
                if (environ == 'CityEnviron'):
                    position = airsim.Vector3r(-214.6370086669922,207.1434326171875,-0.440409541130066)
                    orientation = airsim.utils.to_quaternion(0,0,(90*3.1415)/180)
                    initialPose = airsim.Pose(position,orientation)
        
                    self.__setVehiclePose(initialPose)

                ## Start team Threads
                controlAirSim = False
                if(not(manualMode)):
                    self.getTeam().startThreads()
                
                xvalue = []
                yvalue = []
                
                ## While loop running for updating gas, brake, steering and update. This while only stops when a vehicle 
                ## crashes or team tell they have finished the simulation
                while(not(self.getTeam().hasFinished())):
                    if(not(manualMode)):
                        self.__updateCarControls()
                    self.__updateReport()
                    
                    pose = self.__getVehiclePose()
                    xvalue.append(pose.position.x_val)
                    yvalue.append(pose.position.y_val)
                    plt.title('Vehicle Pose')
                    plt.xlabel('pose x')
                    plt.ylabel('pose y')
                    
                    plt.plot(xvalue,yvalue,'ro')
                    plt.savefig("poseXY.png")
                    
                    if(self.getTeam().getTurnRight()):
                        self.__printMessage("Turn Right ACTIVATED")
                    
                    if(self.getTeam().getTurnLeft()):
                        self.__printMessage("Turn Left ACTIVATED")
                    
                    if(self.getClient().simGetCollisionInfo().has_collided):
                        self.__collisionPrint(self.getClient().simGetCollisionInfo())
                        break

                #plt.plot(xvalue,yvalue)
                #plt.show()
                if(not(manualMode)):
                    self.getTeam().stopThreads()

                self.getTeam().clearVariables()
                time.sleep(5)
                
                #print(position_map)
                ## Puts the vehicle in the initial position
                self.getClient().reset()

                ## Disable Api control
                self.getClient().enableApiControl(False)
                
                ## Close the lauched application
                #if(osys == 'Windows'):
                #    os.system('TASKKILL /F /IM ' + environ + '.exe')
                #elif(osys == 'Linux' or os == 'Darwin'):
                   #os.system('pkill ' + environ + '.exe')
            
        self.__clearVariables()
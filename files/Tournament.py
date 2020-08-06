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

MAZE = 0
AIRSIMNH = 1
BLOCKS = 2
CITY = 3
COASTLINE = 4
LANDSCAPE = 5
SOCCER = 6

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
        return self.getClient().getCarState('Car1').speed
    
    def getIMU_Data(self):
        return self.getClient().getImuData(None,'Car1')
    
    def getLIDAR_Data(self):
        return self.getClient().getLidarData('Lidar','Car1')
    
    def getSONAR_Data(self):
        return self.getClient().getDistanceSensorData(None,'Car1')
    
    def getGPS_Data(self):
        return self.getClient().getGpsData(None,'Car1')
        
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

class Tournament():

    ## =========================== CONSTRUCTORS ==============================         
    
    def __init__(self,team,env = 0):
        self.__setTeam(team)
        self.run(env)
    
    ## ======================= SETTERS AND GETTERS ===========================         
    
    def __setTeam(self,t):
        global team
        team = t
        
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
        
    def getClient(self):
        global client
        return client
    
    def getCarControls(self):
        global car_controls
        return car_controls        
    
    ## ============================= METHODS ================================= 
    
    def __chooseEnvironment(self,env):
        if(env == MAZE):
            unrealEnvironment = 'SimpleMaze'
            environ = 'Car_Maze'
        elif (env == AIRSIMNH):
            unrealEnvironment = 'Neighborhood'
            environ = 'AirSimNH'
        elif (env == BLOCKS):
            unrealEnvironment = 'Blocks'
            environ = unrealEnvironment
        elif (env == CITY):
            unrealEnvironment = 'City'
            environ = 'CityEnviron'
        elif (env == COASTLINE):
            unrealEnvironment = 'Coastline'
            environ = unrealEnvironment
        elif (env == LANDSCAPE):
            unrealEnvironment = 'LandscapeMountains'
            environ = unrealEnvironment
        elif (env == SOCCER):
            unrealEnvironment = 'Soccer_Field'
            environ = unrealEnvironment
        return (unrealEnvironment, environ)
    
    def __airSimClientConnection(self):
        global client, clientCM
        self.__setClient(airsim.CarClient(timeout_value = 10000))
        self.__setClientCM(airsim.VehicleClient())
        self.getClient().confirmConnection()
        self.getClient().enableApiControl(True)
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
        
        throttle = self.getTeam().getGas()
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
        
    def run(self,env):
        osys = platform.system()
        
        ## pathFolder defines the folder that contains your Unreal/Unity Environments
        #pathFolder = 'C:/Users/Gilmar Correia/Downloads/Unreal Environments/'
        if(osys == 'Windows'):
            pathFolder = './Unreal Environments/'
        elif(osys == 'Linux' or os == 'Darwin'):
            pathFolder = './Unreal\ Environments/'
            
        ## Both unrealEnvironment and environ are initializate with the function chooseEnviroment
        unrealEnvironment, environ = self.__chooseEnvironment(env)
        
        ## Defines de resolution that Unreal will start
        resolution = ' -ResX=640 -ResY=480'
            
        ## Executable commands for launch automatically the unrealEnviroment and its respectively environ,
        ## according to AirSim documentation this application can be executable with OpenGL by changing the
        ## -windowed to -opengl
        if(osys == 'Windows'):
            cmdCommand = 'cd ' + pathFolder + unrealEnvironment + '& start ' + environ + resolution + ' -windowed'
        elif(osys == 'Linux' or os == 'Darwin'):
            cmdCommand = 'cd ' + pathFolder + unrealEnvironment + ' && ./' + environ + '.exe' + resolution + ' -windowed'
   
        os.system(cmdCommand) 
        
        ## Variable that control the Unreal launch
        global controlAirSim
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
                #self.getClient().simSetWeatherParameter(airsim.WeatherParameter.Rain, 1.0);
            
                ## Setting Vehicle Initial Pose:
                position = airsim.Vector3r(-214.6370086669922,207.1434326171875,-0.440409541130066)
                orientation = airsim.utils.to_quaternion(0,0,(90*3.1415)/180)
                initialPose = airsim.Pose(position,orientation)
                self.__setVehiclePose(initialPose)
                
                ## Start team Threads
                controlAirSim = False
                self.getTeam().startThreads()
                
                ## While loop running for updating gas, brake, steering and update. This while only stops when a vehicle 
                ## crashes or team tell they have finished the simulation
                while(not(self.getTeam().hasFinished())):
                    self.__updateCarControls()
                    
                    if(self.getClient().simGetCollisionInfo().has_collided):
                        self.__collisionPrint(self.getClient().simGetCollisionInfo())
                        #break
                
                self.getTeam().stopThreads()
                time.sleep(5)
                
                ## Puts the vehicle in the initial position
                self.getClient().reset()

                ## Disable Api control
                self.getClient().enableApiControl(False)
                
                ## Close the lauched application
                if(osys == 'Windows'):
                    os.system('TASKKILL /F /IM ' + environ + '.exe')
                elif(osys == 'Linux' or os == 'Darwin'):
                    os.system('pkill ' + environ + '.exe')
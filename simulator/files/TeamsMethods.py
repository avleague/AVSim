# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 19:43:52 2020

@author: Gilmar Correia
"""
import threading
import abc
import time

#################################################################################        
## =============================== TEAM METHODS ============================== ##        
#################################################################################

threads = [threading.Thread(),threading.Thread(),threading.Thread()]

throttle = 0.0
brake = 0.0
steering = 0.0
        
initialTime = 0.0
finished = False
threadFlag = False

class TeamsMethods(object):
    
    __metaclass__ = abc.ABCMeta   
    
    def __init__(self):
        global threads
        threads[0] = threading.Thread(target=self.longitudinalControl, args=(),daemon = True)
        threads[1] = threading.Thread(target=self.lateralControl, args=(),daemon = True)
        threads[2] = threading.Thread(target=self.update, args=(),daemon = True)
        
    ## ============================= GETTERS AND SETTERS ======================
    
    def setThrottle(self, value):
        global throttle
        throttle = value
    
    def setBrake(self, value):
        global brake
        brake = value
        
    def setSteering(self, value):
        global steering
        steering = value
    
    def getThrottle(self):
        global throttle
        return throttle
    
    def getBrake(self):
        global brake
        return brake
    
    def getSteering(self):
        global steering
        return steering
    
    def getThread(self):
        global thread
        return thread
    
    def getThreadFlag(self):
        global threadFlag
        return threadFlag
        
    ## ================================ METHODS ===============================
    
    def setFinishedFlag(self):
        global finished
        finished = True

    def hasFinished(self):
        global finished
        return finished
    
    def startThreads(self):
        global threads, threadFlag
        threadFlag = True        
        threads[0].start()
        threads[1].start()
        threads[2].start()
    
    def stopThreads(self):
        global threadFlag
        threadFlag = False        
        
    def clearVariables(self):
        global threads, throttle, brake, steering, initialTime, finished, threadFlag
        threads.clear()
        threads = [threading.Thread(),threading.Thread(),threading.Thread()]

        throttle = 0.0
        brake = 0.0
        steering = 0.0
        
        initialTime = 0.0
        finished = False
        threadFlag = False
    ## ============================= ABSTRACT METHODS =========================
    
    @abc.abstractmethod 
    def update(self):
        pass

    @abc.abstractmethod 
    def longitudinalControl(self):
        pass
    
    @abc.abstractmethod 
    def lateralControl(self):
        pass
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 16:26:31 2020

@author: Gilmar Correia
"""
from files.Tournament import CarMethods
from files.TeamsMethods import TeamsMethods

import cv2
import time
import matplotlib.pyplot as plt
import numpy as np

cm = CarMethods()

class Team1(TeamsMethods,object):

    def update(self):
        while self.getThreadFlag():
            #cm.printHomePosition()
            cv2.imshow('my webcam', cm.getCameraShoot())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                pass
                
    def longitudinalControl(self):
        while self.getThreadFlag():
            self.setThrottle(self.getThrottle() + 0.001)
            print('gas: ' + str(self.getThrottle()))
            
    def lateralControl(self):
        while self.getThreadFlag():
            self.setSteering(self.getSteering() + 0.001)
            print('steering: ' + str(self.getSteering()))
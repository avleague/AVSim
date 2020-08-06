# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 16:26:31 2020

@author: Gilmar Correia
"""
from files.Tournament import CarMethods
from files.TeamsMethods import TeamsMethods

import cv2
import time

cm = CarMethods()

class Team1(TeamsMethods,object):

    def gas(self):
        while self.getThreadFlag():
            
            cm.printHomePosition()
            
            self.setGas(self.getGas() + 0.001)
            print('gas: ' + str(self.getGas()))
            
            cv2.imshow('my webcam', cm.getCameraShoot())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                pass
            
    def steering(self):
        while self.getThreadFlag():
            self.setSteering(self.getSteering() + 0.001)
            print('steering: ' + str(self.getSteering()))
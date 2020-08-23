# -*- coding: utf-8 -*-

from files.Tournament import CarMethods
from files.TeamsMethods import TeamsMethods

import cv2
import time

cm = CarMethods()

class sensors(TeamsMethods,object):
    
    def longitudinalControl(self):
        # Insert your code here for longitudinal control #
        pass
        
    def lateralControl(self):
        # Insert your code here for lateral control #
        pass
    
    def update(self):
        # Insert your code here to update values of throttle, brake and steering #
        # or to get sensor data #
        pass
     
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 16:26:31 2020

@author: Gilmar Correia
"""
from files.Tournament import CarMethods
from files.TeamsMethods import TeamsMethods

import time

cm = CarMethods()

class Team2(TeamsMethods,object):
    
    ## ============================== MOVING METHODS ==========================
    
    def goFront(self):
        print("ENTREI")
        self.setGas(0.5)
        self.setSteering(0.0)
        self.setBrake(0.0)
        
    def stop(self):
        print("PAREI")
        self.setGas(0.0)
        self.setSteering(0.0)
        self.setBrake(1.0)
        
    def reverse (self):    
        print("ENTREI")
        self.setGas(-0.5)
        self.setSteering(0.0)
        self.setBrake(0.0)
        
    ## Subscribed methods
    def update(self):
        time.sleep(5)
        self.goFront()
        time.sleep(3)
        self.stop()
        time.sleep(3)
        self.reverse()
        time.sleep(3)
        self.stop()
        time.sleep(3)
        self.setFinishedFlag()
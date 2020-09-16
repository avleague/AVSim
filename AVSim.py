# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 16:34:15 2020

@author: GilmarCorreia
"""

import tkinter as tk
import os
import sys
from importlib import import_module

from tkinter import *
from tkinter import ttk
from files.Tournament import *

from Teams import *


bgColor = '#6942f5'

gui = tk.Tk()
gui.title("AVSim")
gui.geometry("640x420")
gui.configure(background=bgColor)

## mapsPath defines the folder that contains your Unreal/Unity Environments
    #mapsPath = 'C:/Users/Gilmar Correia/Downloads/Unreal Environments/'
mapsPath = './UnrealEnvironments/'
mapsList = [ name for name in os.listdir(mapsPath) if os.path.isdir(os.path.join(mapsPath, name)) ]
maps = ttk.Combobox(gui, values=mapsList)

codePath = './Teams/'
codesList = [ name for name in os.listdir(codePath) if os.path.isfile(os.path.join(codePath, name)) ]
codes = ttk.Combobox(gui, values = codesList)

environ = None

def chooseEnvironment(unrealEnvironment):
    global environ
    if(unrealEnvironment == 'SimpleMaze'):
        environ = 'Car_Maze'
    elif (unrealEnvironment == 'Neighborhood'):
        environ = 'AirSimNH'
    elif (unrealEnvironment == 'City'):
        environ = 'CityEnviron'
    elif (unrealEnvironment == 'Blocks' or unrealEnvironment == 'Coastline' or unrealEnvironment == 'LandscapeMountains' or unrealEnvironment == 'Soccer_Field'):
        environ = unrealEnvironment
    return environ

def launchMap():
    global environ, mapsPath
    osys = platform.system()
        
    ## Both unrealEnvironment and environ are initializate with the function chooseEnviroment
    unrealEnvironment = maps.get()
    environ = chooseEnvironment(unrealEnvironment)
        
    ## Defines de resolution that Unreal will start
    resolution = ' -ResX=640 -ResY=480'
    
    ## Executable commands for launch automatically the unrealEnviroment and its respectively environ,
    ## according to AirSim documentation this application can be executable with OpenGL by changing the
    ## -windowed to -opengl
    if(osys == 'Windows'):
        cmdCommand = 'cd ' + mapsPath + unrealEnvironment + '& start ' + environ + resolution + ' -windowed'
    elif(osys == 'Linux' or os == 'Darwin'):
        cmdCommand = 'cd ' + mapsPath + unrealEnvironment + ' && ./' + environ + '.exe' + resolution + ' -windowed'
   
    os.system(cmdCommand) 
    
def runAVSim():
    global environ
    module = codes.get().replace('.py','')
    exec('Tournament('+module+'.'+module+'(),environ)')
    print('Launch another code!')
    
appTitle = tk.Label(gui, text = "Autonomous Vehicle Simulator", font=("Helvetica", 32), bg = bgColor)
appTitle.pack(fill='both',pady=10)

mapSelector = tk.Label(gui, text = "Select Your Map:", font=("Helvetica", 16), bg = bgColor ,pady = 15)
mapSelector.pack(fill='both',pady=10)

maps.pack()

launchButton = tk.Button(gui, text="LAUNCH", command=launchMap)
launchButton.pack()

codeSelector = tk.Label(gui, text = "Select Your Code:", font=("Helvetica", 16), bg = bgColor ,pady = 15)
codeSelector.pack(fill='both',pady=10)

codes.pack()

runButton = tk.Button(gui, text="RUN", command=runAVSim)
runButton.pack()


    
gui.mainloop()



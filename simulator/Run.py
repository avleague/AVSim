# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 17:10:46 2020

@author: Gilmar Correia
"""

import os
import sys
from importlib import import_module

from files.Tournament import *
from Teams import *

code = sys.argv[1].replace('.py','')

environ = str(sys.argv[2])
operationMode = str(sys.argv[3])

cmd = 'Tournament('+code+'.'+code+'(),"'+environ+'",'+operationMode+')'

if(environ+".exe" in (p.name() for p in psutil.process_iter())):
	exec(cmd)
	print('Launch another code!')
else:	
	print('Launch your environ first')
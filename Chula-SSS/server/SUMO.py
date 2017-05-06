#Chula-sss 20-11-2016 edited by Dr.Kittiphan Techakittiroj & Chonti Krisanachantara
import os					#import module "os", this module provides a portable way of using operating system dependent functionality.
import sys					#import module "sys" this module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
import threading			#import module "threading" this module constructs higher-level threading interfaces on top of the lower level thread module.
import subprocess			#import module "subprocess" this module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
import time					#import module "time" this module provides various time-related functions.
from time import sleep

sys.path.append(os.path.join(os.environ.get('SUMO_HOME'),'tools'))	#go to path 'SUMO_HOME'/tools
sys.path.append(os.path.join(os.environ.get('SUMO_HOME'),'bin'))	#go to Path "SUMO_HOME"/bin

import traci				#import module "traci" this module will allow you to integrate "Trafic Control Interface" with sumo-gui

class SUMO():				#create a class "SUMO"
## This function is to connect to SUMO server.
## Parameter: none.
## Return: none.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj
  def __init__(self, config, add, port, speed):	#takes 4 arguments excluding "self"
    self.config = config						#given 1 argument string    'SUMO/sathorn_w.sumo.cfg' 	 	from "TrafficControl.py" Line '44'
    self.add = add								#given 1 argument string    'SUMO/sathon_wide_tls.add.xml' 	from "TrafficControl.py" Line '45'
    self.port = port							#given 1 argument integer   '2005'				 			from "TrafficControl.py" Line '46'
    self.run = False
    self.speed = speed							#given 1 argument integer   '5' 					 		from "TrafficControl.py" Line '46'
    self.performanceCount = 0
    self.performanceTime = time.time()
    self.getPerformance = 0
    self.getCurrentTime = 0
    self.step = 0

  def _connect(self):
    cmd = ['sumo-gui',									  # cmd = execute sumo-gui in command line with adding necessary option
           '--time-to-teleport','-1',					  # teleporting due to grid-lock is disabled.
           '--lanechange.allow-swap','true',			  # "Solve" issue two vehicles try to get to the other lane, and each vehicle is blocking the other one.
           '--no-internal-links','true',				  # Internal edges are not included if the network was built
           '--ignore-junction-blocker','1',				  # used to ignore vehicles which are blocking the intersection on an intersecting lane after the specified time.
           '--start','true',							  # start the simulation immediately after open sumo-gui
           '--quit-on-end','true',						  # Quits the GUI when the simulation stops; default: false
           '-c', self.config,							  # Loads the named config on startup "self.config" obtain from "TrafficControl.py" Line '44'
           '-a', self.add,								  # Load additional setting from "self.add" obtain from "TrafficControl.py" Line '45'
#          '--game', 'true',							  # Start the GUI in gaming mode; default: false
           '--begin', '54000',							  # Defines the begin time in seconds; The simulation starts at this time; default: 0
#		   '--scale', '0.1',							  # scaling the demand to x
           '--load-state', 'SUMO/state_54000.00.sbx',      	  # load state from 16.00 (James 8 June 2016)
           '--max-depart-delay', '0.1',                   # if a vehicle cannot insert within 1 sec, skip. (James 8 June 2016)
           '--sloppy-insert', 'true',                 	  # sloppy insert (James 8 June 2016)
		   '--no-warnings', 'true',					      # don't show warnings in chula-sss game (James 8 June 2016)
           '--step-length', '0.2',						  # 6 multiple views for the big screen; view #1,2 are not used (James 8 June 2016)
           '--gui-settings-file', 'SUMO/gui-settings-file-overall.xml,SUMO/gui-settings-file-sathorn.xml,SUMO/gui-settings-file-narinthorn.xml,SUMO/gui-settings-file-wittayu.xml',	#Load visualisation settings from FILE
           '--remote-port', str(self.port)]				  # Enables TraCI Server; default: 0
    print cmd;
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)	#execute string "cmd" on command line
    traci.init(self.port)								  #initial Traci with the setting port
    self.run = True
	
	
## This function is to connect to SUMO server. It will crate a separate thread
## Parameter: none.
## Return: none.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj
  def connect(self):									  #Threading to connect SUMO and open GUI at the same time
    thread = threading.Thread(target=self._connect)		  #Threading function _connect from line 28 of SUMO.py
    thread.setDaemon(True)
    thread.start()

## This function is to get the status of the traffic light.
## Parameter: id = the identification of the trafficlight.
## Return: the current status of the traffic light
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj
  def getTrafficLights(self, id):						  #takes 1 arguments excluding "self"
    return traci.trafficlights.getRedYellowGreenState(id) #return current trafficlight state in simulation

## This function is to measure step simulation versus real time
## Parameter: none.
## Return: none.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj
  def stepSimulation(self):
    if (self.run):
      if (self.performanceCount>=100):
        tt = time.time()
        self.getPerformance = self.performanceCount / (tt-self.performanceTime)	#Create a performance of SUMO simulation vs Real time
        self.performanceCount = 0
        self.performanceTime = tt
      traci.simulationStep()
      self.performanceCount += 1
      self.getCurrentTime = traci.simulation.getCurrentTime()/1000.0   

## This function is to  get last step occupancy from sensor
## Parameter: id = identification of sensor.
## Return: the occupancy from the current sensor id.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj
  def getLastStepOccupancy(self, id):
    return traci.inductionloop.getLastStepOccupancy(id)	#Get last step occupancy from each sensor

	
	
## This function is to count vehicle number in each step
## Parameter: id = identification of sensor
## Return: number of vehicle passed that sensor
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj
  def getLastStepVehicleNumber(self, id):	#Count the vehicle number by increment variable "nn"
    ll=traci.inductionloop.getVehicleData(id)
    nn=0
    if (len(ll)>0):
      for i in range(len(ll)):
        if (int(ll[i][3])!=-1):
          nn=nn+1
    return nn

## This function is to set the trafficlight in each junction
## Parameter: id = identification of trafficlight, value = the value of the string of trafficlight
## Return: trafficlight from current value for each id.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj

  def setTrafficLights(self, id, value):	#Set trafficlight according to junction ID and Value = String of trafficlight state
    if (self.run):
      traci.trafficlights.setRedYellowGreenState(id, value)

  def close(self):
    self.run = False
    time.sleep(2)
    traci.close()


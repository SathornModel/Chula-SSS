#Chula-sss 20-11-2016 edited by Dr.Kittiphan Techakittiroj & Chonti Krisanachantara

import wx
import socket
import sys
import threading
import time


########################################################################
class Junction(wx.Frame):

  def _handleUDP(self):
    while self.run:
      data, addr = self.socket.recvfrom(1024)
      if (len(data)==1):
        self.rBox.SetSelection(int(data))
        self.changed=True
      if (len(data)==2):
        self.socket.sendto(self.sInductionLoops.GetLabel(),addr)

  def serverSetup(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.socket.bind(('0.0.0.0',self.portNo))
    thread = threading.Thread(target=self._handleUDP)
    thread.setDaemon(True)
    thread.start()

## This function is to receive information and build UI according to junction name
## Parameter: title, portNo, junctionCode, pos, size, valueList, infoList
## Return: title, portNo, junctionCode, pos, size, valueList, infoList
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj

  def __init__(self, title, portNo, junctionCode, pos, size, valueList, infoList):		# Takes 7 arguments excluding "self" from "TrafficControl.py" line 19-44
    super(Junction, self).__init__(None, -1, title+'('+str(portNo)+')', pos, size)		# Create a GUI frame from __init__ function	give 2 arguments "position of frame" and "size of frame" from TrafficControl.py
    self.run = True
    self.code = junctionCode															#given 1 argument "cluster ID" string from "TrafficControl.py"
    self.listName = [valueList[i] for i in range(0,len(valueList),2)]					#given 1 argument "Trafficlight state ID" string start from "valueList" start from 0 and increment by 2 of all cluster ID from "TrafficControl.py"
    self.listValue = [valueList[i] for i in range(1,len(valueList),2)]					#given 1 argument "Trafficlight state" string start from "valueList" start from 1 and increment by 2 of all cluster ID from "TrafficControl.py"
    self.changed=False
    self.listInfo = infoList															#given 1 argument "inductionloopID" from "TrafficControl.py"
    self.carNumber = [0 for i in range(0,len(infoList))]								#store a car passing sensor in "self.carNumber"
    self.portNo = portNo																#given 1 argument "port" of each junction from "TrafficControl.py"
    self.serverSetup()																	#start a threading server from GUI to control each junction
    self.buildUI()																		
    self.Show()


## This function is to check weather the button is clicked
## Parameter: event = checking if any event occur on button.
## Return: change = true or false.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj

  def buttonClick(self, event):
    self.changed=True


## This function is to build radiobox
## Parameter: listname.
## Return: buttonClick.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj

  def buildUI(self):																		#Build User Interface
    panel = wx.Panel(self, -1)
    self.rBox = wx.RadioBox(panel, label = 'RadioBox', pos=(0,0), choices = self.listName,	#Create a radiobox panel for user interface
                            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
    self.rBox.Bind(wx.EVT_RADIOBOX, self.buttonClick)
    self.sTrafficLights = wx.StaticText(panel, -1, label="", pos=(0, 60))					#Create a static text to show trafficlight state
    self.sInductionLoops = wx.StaticText(panel, -1, label="", pos=(0, 85))					#Create a static text to show Induction loop sensor number

## This function is to show aa current trafficlight state
## Parameter: info.
## Return: label for sTrafficLights.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj

  def setInformationTrafficLight(self, info):		#Create label to show current lightstate
    self.sTrafficLights.SetLabel(info)


## This function is to show number of car passed each sensor
## Parameter: info = inductionloopID.
## Return: sInductionLoops label.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj

  def setInformationTime(self, info):
    value = str(info)
    value = value + "," + str(self.rBox.GetSelection())
    for k in range(len(self.listInfo)):							#counting a number of a car passed each sensor
      value = value+","+str(self.carNumber[k])
    self.sInductionLoops.SetLabel(value)						#displaying a number of a car passed each sensor
   
## This function is to show each induction loop name
## Parameter: none.
## Return: listinfo = inductionloopID.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj
  def getIndexInductionLoop(self):
    return self.listInfo

## This function is to get value from selected value from radiobox
## Parameter: none.
## Return: listValue.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj
  def getValue(self):											#Return the selected radiobox value to store in listValue
    return self.listValue[self.rBox.GetSelection()]
    
## This function is to exit program
## Parameter: none.
## Return: run = boolean.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj
  def exitProgram(self):
    self.run = False
    self.socket.close()
    self.Destroy()

## This function is to check if tmp is change
## Parameter: none.
## Return: tmp = boolean.
## Version: 1
#### 2016-12-20 Created by Chonti Krisanachantara
#### 2016-12-24 Commented by Kittiphan Techakittiroj
  def isChange(self):
    tmp=self.changed
    self.changed=False
    return tmp
    


#Chula-sss 20-11-2016 edited by Dr.Kittiphan Techakittiroj & Chonti Krisanachantara
import wx
import functools
import threading
import time
import SUMO
import Junction


########################################################################
class Control(wx.Frame):

  def __init__(self, parent, title):
    global sathornModel
    print threading.activeCount()
    super(Control, self).__init__(None, -1, 'Sathorn Model', pos=(0,0), size=(600, 450))	#Main GUI name = "Sathorn Model" at Position = (0,0) size = 600x450 pixel
    self.buildUI()
    self.Show()
    # Create junctions
    self.junction=[]	#given self.junction string value = empty
    self.junction.append( Junction.Junction('Surasak', 4600, 'cluster_46_47', (0,600), (400,140),	#title, portNo, junctionCode, pos, size
      ['000000', 'GGGGrrrrGGGGGGGGGGGGGGGGGGGGrrrrrrrrrrrrrGGGGGGGGGGGGGGGG',						#Trafficlight state ID, Trafficlight state
       '111111', 'GGGGGGGGGrrrrrrrrrrrrrrrrGGGrrrrrrrGGGGGGrrrrrrrrrrrrrrrr',						#Trafficlight state ID, Trafficlight state
       '222222', 'rrrrrrrrrrrrrrrrrrrrrrrrrGGGGGGGGGGGGGGGGrrrrrrrrrrrrrrrr'],						#Trafficlight state ID, Trafficlight state
      ["00","01","02","03","10","11","12","13","14","20","21","22","23","30","31","32","33"]))		#inductionloop sensor ID at Wittayu Intersection
    self.junction.append( Junction.Junction('Narinthorn', 2100, 'cluster_20_21_22_23', (400,600), (800,140),	#title, portNo, junctionCode, pos, size
      ['000000', 'gggrrrrrrrrrrrrrgrrrrrrrrrrrrrrrrggrrrrrrrrrrrrrrgGGGGGGGGGGGGGGGGGGGG',						#Trafficlight state ID, Trafficlight state
       '111111', 'gggrrrrrrrrrrrrrgrrrrrrrrrrrrrrrrggGGGGGGGGGGGGGGgrrrrrrrrrrrrrrrrrrrr',						#Trafficlight state ID, Trafficlight state
       '222222', 'gggGGGGGGGGGGGGGgrrrrrrrrrrrrrrrrggrrrrrrrrrrrrrrgrrrrrrrrrrrrrrrrrrrr',						#Trafficlight state ID, Trafficlight state
       '333333', 'gggrrrrrrrrrrrrrgGGGGGGGGGGGGGGGGggrrrrrrrrrrrrrrgrrrrrrrrrrrrrrrrrrrr',						#Trafficlight state ID, Trafficlight state
       '444444', 'gggrrrrrrrrrrrrrgGGGGGGGGGGGGGGGGggrrrrrrrrrrrrrrgGGGGGGGGGGGGrrrrrrrr'],						#Trafficlight state ID, Trafficlight state
      ["34","35","36","37","38",  "39","40","41","42",  "43","44","45","46","47",  "48","49","50","51","52"]))	#inductionloop sensor ID at Wittayu Intersection
    self.junction.append( Junction.Junction('Wittayu', 13400, 'cluster_134_135_136_138', (0,700), (1200,140),	#title, portNo, junctionCode, pos, size
      ['000000', 'rrrrrrGGGGGGGGGGGGGrrrrrrrrrrrrrrrrrrrrrrrrr',									#Trafficlight state ID, Trafficlight state
       '111111', 'GGGGGGrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',									#Trafficlight state ID, Trafficlight state
       '222222', 'GGrrrrrrrrrrrrrrrrrGGGGGGrrrrrrrrrrrrrrrrrrr',									#Trafficlight state ID, Trafficlight state
       '333333', 'rrGGGGrrrrrrrrrrrrrrrrrrrGGGGGGrrrrrrrrrrrrr',									#Trafficlight state ID, Trafficlight state
       '444444', 'rrrrrrGGGGGGGGGrrrrrrrrrrrrrrrrGGGGGGrrrrrrr',									#Trafficlight state ID, Trafficlight state
       '555555', 'rrrrrrrrrrrrrrrGGGGrrrrrrrrrrrrrrrrrrGGGGGGG',									#Trafficlight state ID, Trafficlight state
       '666666', 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrGGGGGGGGGGGGG',									#Trafficlight state ID, Trafficlight state
       '777777', 'rrrrrrrrrrrrrrrrrrrGGGGGGGGGGGGrrrrrrrrrrrrr'],									#Trafficlight state ID, Trafficlight state
      ["53","54","55","56","57",  "58","59","60",  "61","62","63","64","65",  "66","67","68","69"]))#inductionloop sensor ID at Wittayu Intersection
    # Connect SUMO
    sathornModel=SUMO.SUMO('SUMO/sathorn_w.sumo.cfg',	   #initialize string "self.config" 		in class SUMO of SUMO.py
                           'SUMO/sathon_wide_tls.add.xml', #initialize "self.add"					in class SUMO of SUMO.py
                           2005, 5)						   #initialize "self.port", "self.speed" 	in class SUMO of SUMO.py
    self.timer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.updateTimer, self.timer)
    self.timer.Start(185)
    sathornModel.connect()	#sathornModel connect as a threading from SUMO

  def buildUI(self):
    panel = wx.Panel(self, -1)	#Create panel in User Interface
    sizer = wx.BoxSizer(wx.VERTICAL)
    # Logo
    button = wx.BitmapButton(panel, id=wx.ID_ANY,	#Create sathorm model logo on main GUI from media/logo.png, size= 200x200 pixel, position = 32,20
                             bitmap=wx.Bitmap("media/logo.png", wx.BITMAP_TYPE_ANY),
                             size=(200, 200))
    button.SetPosition((32,20))
    # Simulation Speed
    self.rBox = wx.RadioBox(panel, label = 'Simulation Speed', pos=(0,230),	#Create Radiobox with radiobutton 8 cases
                            choices = ['x1 ','x2 ','x4 ','x8 ','x16 ','x32 ','x64 ','x128 '],	#8 cases
                            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
	# set the simulation speed to x4 (James 9 June 2016)
    self.rBox.SetSelection(2)	
    # Traffic Lights Status
    self.runSimTime = wx.StaticText(panel, -1, label="", pos=(10,300))
    self.runSimPerformance = wx.StaticText(panel, -1, label="", pos=(10,325))
    # Exit Button
    name = 'EXIT'
    button = wx.Button(panel, -1, name,pos =(400,300),size=(60,30))
    button.Bind(wx.EVT_BUTTON, functools.partial(self.exitProgram, button=name))
    sizer.Add(button, 0, wx.ALL, 5)


  def _updateTimerPreProcessing(self):	#Update trafficlight signal when its changed
    for j in range(len(self.junction)):
      if self.junction[j].isChange():		
        sathornModel.setTrafficLights(self.junction[j].code, self.junction[j].getValue())

  def _updateTimerPostProcessing(self):	#Show current state and current time
    for j in range(len(self.junction)):
      self.junction[j].setInformationTrafficLight(sathornModel.getTrafficLights(self.junction[j].code))
      self.junction[j].setInformationTime(sathornModel.getCurrentTime)

  def updateTimer(self, event):			#Update information for each simulation step
    global sathornModel
    if (sathornModel.run):
      self._updateTimerPreProcessing()
      for i in range(0, 2**(self.rBox.GetSelection())):
        sathornModel.stepSimulation()							
        for j in range(len(self.junction)):
          ii=self.junction[j].getIndexInductionLoop()
          for k in range(len(ii)):								#Increment of a car number counting by getLastStepVehicleNumber
            self.junction[j].carNumber[k]+=int(sathornModel.getLastStepVehicleNumber(ii[k]))     
      self.runSimTime.SetLabel("Simulation Time (s): " + '{:.2f}'.format(sathornModel.getCurrentTime))
      self.runSimPerformance.SetLabel("Performance (SUMO run/s): " + '{:.4f}'.format(sathornModel.getPerformance))
      self._updateTimerPostProcessing()

  def exitProgram(self, event, button):
    global sathornModel
    for i in range(len(self.junction)):
      self.junction[i].exitProgram()
    sathornModel.close()
    self.Destroy()


########################################################################
app = wx.App(False)
Window_exec = Control(None, title='')
app.MainLoop()

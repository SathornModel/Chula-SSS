#Chula-sss 20-11-2016 edited by Dr.Kittiphan Techakittiroj & Chonti Krisanachantara
import wx
import wxArt
import threading
import socket
import functools
import time
import matplotlib
import csv

matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
import pylab

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook


class Intersection(wx.Frame):
  title="Surasak Intersection"	#Give a title name for user interface of Surasak Intersection
  def __init__(self):				#Initialize parameter of class Intersection
    super(Intersection, self).__init__(None, -1, self.title, size=(960, 1080))		#Set a name and size of windows that appear for as a user interface
    self.IP='127.0.0.1'																#Set ip as a local IP address *You can change it to your access point
    self.PORT=4600																	#Set port as 4600
    self.run = True
    self.resetGraph = True
    #self.ShowFullScreen(True)
    self.buildUI()
    self.Show()
    self.serverSetup()
    self.timer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.updateTimer, self.timer)
    self.timer.Start(500)
    self.g0=0																		#set g0 as a dummy variable = 0
    self.g1=0																		#set g1 as a dummy variable = 0
    self.data=""																	#Initialize self.data = empty

  def serverSetup(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.socket.bind(('0.0.0.0',self.PORT+1))
    thread = threading.Thread(target=self._handleUDP)
    thread.setDaemon(True)
    thread.start()
                    
  def updateTimer(self,event):
    if self.run:
      if (len(self.data)>5):
        global init_x0, init_y0, init_y1											#globalize x0,y0,y1
        self.readValue.SetLabel(self.data)											#setLabel for self.data
        tmp=self.data.split(',')													#tmp receive from Junction.py and change everytime there is a change, and split by ',' for each string
        yek = [ (int(tmp[2])+int(tmp[3])+int(tmp[4])+int(tmp[5])),					#to make each data from "tmp" becoming integer and store into "yek" each direction split by ',' for vehicles number
                (int(tmp[6])+int(tmp[7])+int(tmp[8])+int(tmp[9])+int(tmp[10])),
                (int(tmp[11])+int(tmp[12])+int(tmp[13])+int(tmp[14])),
                (int(tmp[15])+int(tmp[16])+int(tmp[17])+int(tmp[18])) ]
        self.readValueProcessed.SetLabel(str(yek[0])+' '+str(yek[1])+' '+			#Set label for data "yek"[0-3]
                                         str(yek[2])+' '+str(yek[3]))
        if (self.resetGraph):
          init_x0=float(tmp[0])														#initialize x0= current stepSimulation
          init_y0=float(yek[self.g0])
          init_y1=float(yek[self.g1])
          self.data_x=[]															#Initialize self.data_x= empty array
          self.data1_y=[]															#Initialize self.data1_y= empty array
          self.data2_y=[]															#Initialize self.data2_y= empty array
          self.resetGraph=False
        self.simtime.SetValue(tmp[0])												#initialize self.simtime = tmp[0] *current simulation time
        tt = float(tmp[0])-init_x0
        self.data_x.append(tt)														#self.data_x append number "tt" as a data group
        self.data1_y.append(yek[self.g0]-init_y0)
        self.data2_y.append(yek[self.g1]-init_y1)
        self.durtimer.SetLabel(str(tt))												#Setlabel for the duration the phasing have been changed
        self.simtime1.SetLabel(tmp[0])												#Setlabel for the duration of the simulation time
   
        if ((len(self.data_x)%5)==4):
          self.fig.clf()
          axes1 = self.fig.add_subplot(121)											#add graph 1x2 store in graph 1  from Surasak , South Sathorn
          axes1.set_axis_bgcolor('white')											#set graph background color
          axes1.grid(True, color='GREY')											#add grid by top
          axes1.set_xlabel('Time(s)',size = 15)										#set label on x axes
          axes1.set_ylabel('Vehicles/Hour', size=15)								#set label on y axes
          axes1.set_title('Surasak,North Sathorn', size=15)							#set title of the graph
		  
          axes2 = self.fig.add_subplot(122)											#add graph 1x2 store in graph 2 from Charoenrat , South Sathorn
          axes2.set_axis_bgcolor('white')											#set graph background color
          axes2.grid(True, color='GREY')											#add grid by top
          axes2.set_xlabel('Time(s)',size = 15)										#set label on x axes
          axes2.set_title('Charoenrat,South Sathorn', size=15)						#set title of the graph
		  
          axes1.axis([0, 300, 0, 600])												#Set initial range of x axes 0-300, y axes 0-600 for graph number 1
          axes2.axis([0, 300, 0, 600])												#Set initial range of x axes 0-300, y axes 0-600 for graph number 2
          axes1.plot([0, 300], [0, 300*1.5], color='green', lw=2)					#Set permanent ploted as a green color or "optimum vehicles/hour line"
          axes1.plot(self.data_x, self.data1_y, color='black', lw=2)				#plot real time graph from simulator for vehicles/hour
          if (self.g0!=self.g1):													#if self.g0 and self.g1 are the same number that mean only one graph have to be appear because only one road have green signal
            axes2.plot([0, 300], [0, 300*1.5], color='green', lw=2)					#Set permanent ploted as a green color or "optimum vehicles/hour line"
            axes2.plot(self.data_x, self.data2_y, color='black', lw=2)				#plot real time graph from simulator for vehicles/hour
          self.canvas.draw()
        self.data=""
      self.socket.sendto("G0",(self.IP,self.PORT))

  def _handleUDP(self):
    while self.run:
      self.data, addr = self.socket.recvfrom(1024)			#self.data receive from Junction.py

  def onChangeButton(self, event, button):
    # Clearing Button
    j=-1
    for i in range(len(self.button)):						#Unknown
      if (i!=button):
        self.button[i].SetValue(False)
    self.valueToSend.SetLabel(str(button))
    self.socket.sendto(str(button),(self.IP,self.PORT))
    if (button==0):											#Both North Sathorn and South Sathorn having green signal
      self.plan.SetLabel('0 -- North Sathorn - South Sathorn')
      self.g0 = 3
      self.g1 = 1
    if (button==1):											#Both Surasak and Charoenrat having green signal
      self.plan.SetLabel("1 -- Surasak - Charoenrat")
      self.g0 = 2
      self.g1 = 0
    if (button==2):											#Only Surasak having green signal
      self.plan.SetLabel("2 -- Surasak")
      self.g0 = 2
      self.g1 = 2
    self.resetGraph = True
      
  def buttonClick(self, event, button):
    if (button==-1):
      self.run=False
      time.sleep(2)
      self.socket.close()
      self.Destroy()
    
  def init_plot(self):
    self.fig = Figure((9.5, 5), dpi=100)											#Set figure of the plot by size and dot per inches

  def buildUI(self):											#building user interface for plotting and trafficlight button
    self.panel = wx.Panel(self, -1)
    sizer = wx.BoxSizer(wx.VERTICAL)
	#set background
    file0="pic/traffic.jpg"										#import picture "traffic.jpg" from folder "pic"
    self.bg = wx.StaticBitmap(self.panel,-1,					#convert file0 to bitmap and scaled it to 960x1060 (for TV)
                wx.Image(file0,wx.BITMAP_TYPE_JPEG).Scale(960,1060).ConvertToBitmap(),(0,0))
    
    self.init_plot()											#Initialze plotting
    self.canvas = FigCanvas(self.panel, -1, self.fig)


    self.button = [ wxArt.ToggleButton(self.bg, -1,'pic/surasak/surasak_1.png','pic/surasak/surasak_1_on.png',(50,720),(125, 125)),	#Using toggle button from wxArt and import both "on" and "off" picture
                    wxArt.ToggleButton(self.bg, -1,'pic/surasak/surasak_2.png','pic/surasak/surasak_2_on.png',(190,720),(125, 125)),
                    wxArt.ToggleButton(self.bg, -1,'pic/surasak/surasak_3.png','pic/surasak/surasak_3_on.png',(330,720),(125, 125))]
    for i in range(len(self.button)):	#Make self.button functioning as a toggle button
      func = functools.partial(self.onChangeButton, button=i)
      self.button[i].Bind(wxArt.EVT_BUTTON, func)
      self.button[i].SetValue(False)	

    #self.plan = wx.StaticText(self.panel, -1, label="Current Plan: ",pos =(10,260))
    self.plan = wx.StaticText(self.panel, -1, label="",pos =(230,510))	#set self.plan for "plan nummber" of the trafficlight
    font = wx.Font(25, wx.DEFAULT, wx.NORMAL, wx.NORMAL)				#set font parameter
    self.plan.SetFont(font)												#Set plan font as font
	
    #self.timer = wx.StaticText(self.panel, -1, label="Current Time: ",pos =(10,290))
    self.simtime = wx.TextCtrl(self.bg, -1, "", pos=(10,1120))							#Showing simulation time as a textctrl
    self.simtime1 = wx.StaticText(self.bg, -1, "Simulation Time", pos=(240,550))		#Showting "Simulation" as a statictext 
    self.simtime1.SetFont(font)															#Set simtime1 font as font

    self.target=wx.StaticText(self.panel, -1, label="Target Time",pos =(515,590))		#self.target set "Target Time" as a statictext
    self.target.SetFont(font)															#set target font as font
	
    self.durtimer = wx.StaticText(self.panel, -1, label="0.0",pos =(500,640))			#self.durtimer set "0.0" as a static text (duration timer)
    #self.phasedur = wx.TextCtrl(self.panel, -1, "", pos=(250,320),size=(50, -1))
    self.durtimer.SetFont(font)															#durtimer font as font

    button = wx.Button(self.panel, -1, 'Exit',pos =(400,690),size=(40,40))				#Set button for "exit"
    func = functools.partial(self.buttonClick, button=-1)
    button.Bind(wx.EVT_BUTTON, func)
    sizer.Add(button, 0, wx.ALL, 5)

    self.valueToSend = wx.StaticText(self.panel, -1, label="0",pos =(10,1150))			#still unknown
    self.readValue = wx.StaticText(self.panel, label="0",pos =(10,1170))				#still unknown
    self.readValueProcessed = wx.StaticText(self.panel, label="0",pos =(10,1190))		#still unknown

app = wx.App(False)
locale = wx.Locale(wx.LANGUAGE_ENGLISH)
Window_exec = Intersection()
app.MainLoop()

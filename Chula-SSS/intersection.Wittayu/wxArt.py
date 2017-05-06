import wx
import wx.lib.newevent

ButtonEvent, EVT_BUTTON = wx.lib.newevent.NewCommandEvent()

class ToggleButton(wx.BitmapButton):
  def __init__(self, parent, id, file0, file1, pos=wx.DefaultPosition,
               size=wx.DefaultSize, style=0):
    self.ico = [wx.Image(file0,wx.BITMAP_TYPE_PNG).
                   Scale(size[0]*0.7,size[1]*0.7).ConvertToBitmap(),
                wx.Image(file1,wx.BITMAP_TYPE_PNG).
                   Scale(size[0]*0.7,size[1]*0.7).ConvertToBitmap()]
    super(ToggleButton,self).__init__(parent, id, self.ico[0], pos, size, style)
    self.SetValue(False)
    self.Bind(wx.EVT_BUTTON, self.onClick)
    self.enabled=True

  def SetValue(self, val):
    self.value = val
    if (self.value):
      super(ToggleButton,self).SetBitmapLabel(self.ico[1])
    else:
      super(ToggleButton,self).SetBitmapLabel(self.ico[0])

  def GetValue(self):
    return self.value

  def Enable(self, val):
    self.enabled=val

  def onClick(self,event):
    if (self.enabled):
      if (self.value):
        self.SetValue(False)
      else:
        self.SetValue(True)
      evt = ButtonEvent(self.GetId())
      self.GetEventHandler().ProcessEvent(evt)

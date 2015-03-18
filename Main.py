import wx
from Resources.constants import *
from Resources.Audio import *
from Resources.CtrlPanel import *
from Resources.ImageAnalisis import *
from Resources.MainPanel import *

class MyFrame(wx.Frame):
    def __init__(self, parent, title, pos, size):
        wx.Frame.__init__(self, parent, -1, title, pos, size)
        self.panel = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.tab = SndTable(None)
        self.src = Looper(self.tab)
        self.fx= [Fx(self.src).stop() for i in range(MAX_NUM_LINES)]
        self.control = ControlPanel(self.panel, fxp1=self.fx, fxp2=self.fx, fxp3=self.fx)
        self.MainPanel = MainPanel(self.panel, size=imsize, fxp1=self.fx, fxp2=self.fx, fxp3=self.fx)
        box.Add(self.control, 0, wx.ALL, 5)
        box.Add(self.MainPanel, 1, wx.ALL, 0)
        self.panel.SetSizerAndFit(box)

app = wx.App()
frame = MyFrame(None,title="Image Reader",pos=(100,100), size=(imsize[0]+150,imsize[1]+20))
frame.Show()
app.MainLoop()
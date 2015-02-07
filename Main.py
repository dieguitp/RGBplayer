import wx
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
        self.fxr = [Fx(self.src).stop() for i in range(1)]
        self.fxg = [Fx(self.src).stop() for i in range(1)]
        self.fxb = [Fx(self.src).stop() for i in range(1)]
        self.control = ControlPanel(self.panel, fxr=self.fxr, fxg=self.fxg, fxb=self.fxb)
        self.MainPanel = MainPanel(self.panel, size=imsize, fxr=self.fxr, fxg=self.fxg, fxb=self.fxb)
        box.Add(self.control, 0, wx.ALL, 5)
        box.Add(self.MainPanel, 1, wx.ALL, 0)
        self.panel.SetSizerAndFit(box)

app = wx.App()
frame = MyFrame(None,title="Image Reader",pos=(100,100), size=(imsize[0]+150,imsize[1]+20))
frame.Show()
app.MainLoop()
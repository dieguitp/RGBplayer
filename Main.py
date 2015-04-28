import wx, time
from Resources.constants import *
from Resources.Audio import *
from Resources.CtrlPanel import *
from Resources.ImageAnalisis import *
from Resources.MainPanel import *

class MyFrame(wx.Frame):
    def __init__(self, parent, title, pos, size):
        wx.Frame.__init__(self, parent, -1, title, pos, size)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.panel = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.Audio = audioSrc(None)
        self.snd = self.Audio.output
        self.fx= [Fx(self.snd).stop() for i in range(MAX_NUM_LINES)]
        self.control = ControlPanel(self.panel, fxp1=self.fx, fxp2=self.fx, fxp3=self.fx)
        self.MainPanel = MainPanel(self.panel, size=imsize, fxp1=self.fx, fxp2=self.fx, fxp3=self.fx)
        box.Add(self.control, 0, wx.ALL, 5)
        box.Add(self.MainPanel, 1, wx.ALL, 0)
        self.panel.SetSizerAndFit(box)
        
        self.CreateStatusBar()
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_ABOUT, '&About',
                         '')
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, 'E&xit', 'Exit the application')
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        self.SetMenuBar(menu_bar)
        self.Show()

        

    def OnClose(self, evt):
        self.control.OnClose()
        time.sleep(0.2)
        self.Destroy()
        
app = wx.App()
frame = MyFrame(None,title="RGBPlayer",pos=(100,100), size=(imsize[0]+150,imsize[1]+20))
frame.Show()
app.MainLoop()
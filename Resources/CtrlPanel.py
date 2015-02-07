import wx, os
from pyo import *

s=Server().boot()

wildcard = "AIF (*.aif)|*.aif;*.aiff|"     \
           "WAV (*.wav)|*.wav;*.wave;*.WAV|" \

class ControlPanel(wx.Panel):
    def __init__(self, parent, fxr=None, fxg=None, fxb=None):
        wx.Panel.__init__(self, parent)
        self.StartStopText = wx.StaticText(self, id=-1, label="Path", pos=(10,10), size=wx.DefaultSize)
        self.StartStop = wx.ToggleButton(self, id=-1, label="Start / Stop", pos=(2,28), size=wx.DefaultSize)
        self.StartStop.Bind(wx.EVT_TOGGLEBUTTON, self.handleAudio)
        self.fxr = fxr
        self.fxg = fxg
        self.fxb = fxb        
        Effects= ['-- None --', 'FM', 'BP', 'Distortion', 'Reverb', 'Delay']
        
        self.RedChoiceText = wx.StaticText(self, id=-1, label="Red Effect", pos=(10,100), size=wx.DefaultSize)
        self.RedChoice = wx.Choice(self, id=-1, pos=(2,118), size=wx.DefaultSize, choices=Effects)
        self.RedChoice.Bind(wx.EVT_CHOICE, self.changeFxR)
        self.GreenChoiceText = wx.StaticText(self, id=-1, label="Green Effect", pos=(10,150), size=wx.DefaultSize)
        self.GreenChoice = wx.Choice(self, id=-1, pos=(2,168), size=wx.DefaultSize, choices=Effects)
        self.GreenChoice.Bind(wx.EVT_CHOICE, self.changeFxG)
        self.BlueChoiceText = wx.StaticText(self, id=-1, label="Blue Effect", pos=(10,200), size=wx.DefaultSize)
        self.BlueChoice = wx.Choice(self, id=-1, pos=(2,218), size=wx.DefaultSize, choices=Effects)
        self.BlueChoice.Bind(wx.EVT_CHOICE, self.changeFxB)

        b = wx.Button(self, -1, "Open sound file", (2,58))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()

            self.GetParent().GetParent().tab.setSound(path)
            dur = self.GetParent().GetParent().tab.getDur()
            self.GetParent().GetParent().src.setDur(dur)

        dlg.Destroy()

        
    def handleAudio(self, evt):
        if evt.GetInt() == 1:
            self.GetParent().GetParent().MainPanel.timer.Start(50)
            s.start()
        else:
            self.GetParent().GetParent().MainPanel.timer.Stop()
            s.stop()
            
    def changeFxR(self, evt):
        for i in range(8):
            self.fxr[i].changeFx(evt.GetString())
        
    def changeFxG(self, evt):
        for i in range(8):
            self.fxg[i].changeFx(evt.GetString())
        
    def changeFxB(self, evt):
        for i in range(8):
            self.fxb[i].changeFx(evt.GetString())
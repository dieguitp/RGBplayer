import wx, os
from pyo import *

s=Server().boot()

wildcard = "AIF (*.aif)|*.aif;*.aiff|"     \
           "WAV (*.wav)|*.wav;*.wave;*.WAV|" \

class ControlPanel(wx.Panel):
    def __init__(self, parent, fxp1=None, fxp2=None, fxp3=None):
        wx.Panel.__init__(self, parent)
        self.StartStopText = wx.StaticText(self, id=-1, label="Path", pos=(10,10), size=wx.DefaultSize)
        self.StartStop = wx.ToggleButton(self, id=-1, label="Start / Stop", pos=(2,28), size=wx.DefaultSize)
        self.StartStop.Bind(wx.EVT_TOGGLEBUTTON, self.handleAudio)
        self.fxp1 = fxp1
        self.fxp2 = fxp2
        self.fxp3 = fxp3    
        Effects= ['-- None --', 'FM', 'BP', 'Distortion', 'Reverb', 'Delay', 'Ring Modulation',
         'Flanger', 'Vocoder']
        
        self.choiceText = wx.StaticText(self, id=-1, label="Effect", pos=(10,100), size=wx.DefaultSize)
        self.choice = wx.Choice(self, id=-1, pos=(2,118), size=wx.DefaultSize, choices=Effects)
        self.choice.Bind(wx.EVT_CHOICE, self.changeFx)

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
            
    def changeFx(self, evt):
        for i in range(1):
            self.fxp1[i].changeFx(evt.GetString())
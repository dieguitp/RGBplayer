import wx, os
from pyo import *

s=Server(duplex=1).boot()

wildcard = "AIF (*.aif)|*.aif;*.aiff|"     \
           "WAV (*.wav)|*.wav;*.wave;*.WAV|" \

class ControlPanel(wx.Panel):
    def __init__(self, parent, fxp1=None, fxp2=None, fxp3=None):
        wx.Panel.__init__(self, parent)
        self.StartStopText = wx.StaticText(self, id=-1, label="Path", pos=(10,12), size=wx.DefaultSize)
        self.StartStop = wx.ToggleButton(self, id=-1, label="Start / Stop", pos=(2,28), size=wx.DefaultSize)
        self.StartStop.Bind(wx.EVT_TOGGLEBUTTON, self.handleAudio)
        self.fxp1 = fxp1
        self.fxp2 = fxp2
        self.fxp3 = fxp3    
        Effects= ['-- None --', 'FM', 'BP', 'Distortion', 'Reverb', 'Delay', 'Ring Modulation',
         'Flanger', 'Vocoder', 'Phaser']
        
        self.choiceText = wx.StaticText(self, id=-1, label="Effect", pos=(10,126), size=wx.DefaultSize)
        self.choice = wx.Choice(self, id=-1, pos=(2,140), size=wx.DefaultSize, choices=Effects)
        self.choice.Bind(wx.EVT_CHOICE, self.changeFx)
        
        SRC = ['Sound File', 'Record Clip', 'Live from microphone']
        self.choiceText = wx.StaticText(self, id=-1, label="Sound Source", pos=(10,86), size=wx.DefaultSize)
        self.choice = wx.Choice(self, id=-1, pos=(2,102), size=wx.DefaultSize, choices=SRC)
        self.choice.Bind(wx.EVT_CHOICE, self.changeSrc)
        
        self.b = wx.Button(self, -1, "Open sound file", (2,58))
        self.b.Bind(wx.EVT_BUTTON, self.OnButton, self.b)
            
        self.c = wx.Button(self, -1, "Clip Record", (2,58))
        self.c.Bind(wx.EVT_BUTTON, self.OnButtonRec, self.c)
        self.c.Hide()

        self.m = wx.ToggleButton(self, -1, "Arm microphone", (2,58))
        self.m.Bind(wx.EVT_BUTTON, self.MicConnect, self.m)
        self.m.Hide()

        self.slidervol = wx.Slider(self, -1, 1000, 0, 1000, (50, 200), (50, 100),
        wx.SL_VERTICAL | wx.SL_INVERSE)
        self.Bind(wx.EVT_SLIDER, self.handleGlobalAmp, self.slidervol)

    def handleGlobalAmp(self, evt):
        s.amp = evt.GetInt() * 0.001

    def OnClose(self):
        if s.getIsStarted():
            s.stop()

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

            self.GetParent().GetParent().Audio.setSound(path)

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
            
    def OnButtonRec(self, evt):
        self.GetParent().GetParent().Audio.starttabrec()
        
    def MicConnect(self, evt):
        x=1
            
    def changeSrc(self, evt):
        self.GetParent().GetParent().Audio.srcout(evt.GetString())
        if evt.GetString() == 'Sound File':
            self.b.Show()
            self.c.Hide()
            self.m.Hide()
        elif evt.GetString() == 'Record Clip':
            self.c.Show()
            self.b.Hide()
            self.m.Hide()
        elif evt.GetString() == 'Live from microphone':
            #self.m.Show()
            self.b.Hide()
            self.c.Hide()

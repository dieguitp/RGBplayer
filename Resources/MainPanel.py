import wx, os
from constants import *

class MainPanel(wx.Panel):
    def __init__(self, parent, bg_img='Im.png', size=wx.DefaultSize, fxp1=None, fxp2=None, fxp3=None):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetMinSize(size)
        self.fxp1 = fxp1
        self.fxp2 = fxp2
        self.fxp3 = fxp3
        self.points = []
        self.current = 0
        self.tpos = []
        self.selected = None
        self.selectedPos = wx.Point(0,0)
        self.selectedLine = []
        self.bg = wx.Bitmap(bg_img)
        self.img = wx.Image(bg_img, wx.BITMAP_TYPE_PNG)
        self._width, self._height = self.bg.GetSize()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        
        self.timer = wx.Timer(self)

    def OnEraseBackground(self, evt):
        pass

    def OnRightDown(self, evt):
        which = -1
        pos = evt.GetPosition()
        for i, line in enumerate(self.points):
            x, y = line[0].Get()
            rect = wx.Rect(x-5, y-5, 10, 10)
            if rect.Contains(pos):
                which = i
        if which != -1:
            l = []
            for i, line in enumerate(self.points):
                if i != which:
                    l.append(line)
            self.points = l
            self.Refresh()
                
    def OnLeftDown(self, evt):
        pos = evt.GetPosition()
        if len(self.points) > 0:
            for i, line in enumerate(self.points):
                x, y = line[0].Get()
                rect = wx.Rect(x-5, y-5, 10, 10)
                if rect.Contains(pos):
                    self.selected = i
                    self.CaptureMouse()
                    self.selectedPos = line[0]
                    self.selectedLine = line
                    return
        if len(self.points) < MAX_NUM_LINES:
            # une nouvelle traj start le FX
            pos = len(self.points)
            if self.fxp1[pos] != None:
                self.fxp1[pos].out()
            self.points.append([])
            self.current = len(self.points) - 1
            self.tpos.append(0)
            self.points[self.current].append(evt.GetPosition())
            self.CaptureMouse()
            self.Refresh()
        
    def OnLeftUp(self, evt):
        self.selected = None
        if self.HasCapture():
            self.ReleaseMouse()

    def OnMotion(self, evt):
        if self.HasCapture():
            if self.selected != None:
                pos = evt.GetPosition()
                diff = pos - self.selectedPos
                l = []
                for pt in self.selectedLine:
                    l.append(pt + diff)
                self.points[self.selected] = l
            else:
                self.points[self.current].append(evt.GetPosition())
            self.Refresh()
        
    def OnPaint(self, evt):
        w,h = self.GetSize()
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.DrawRectangle(0,0,w,h)
        dc.DrawBitmap(self.bg, 0, 0)
        dc.SetPen(wx.Pen("#FF0000", width=5))
        dc.SetBrush(wx.Brush("#FF0000", style=wx.TRANSPARENT))
        for i in range(len(self.points)):
            if len(self.points[i]) >= 2:
                x, y = self.points[i][0].Get()
                dc.DrawRoundedRectangle(x-5, y-5, 10, 10, 1)
                dc.DrawLines(self.points[i])
                pos = self.points[i][self.tpos[i]]
                dc.DrawCirclePoint(pos, 6)
                
    def OnTimer(self,evt):
        for i in range(len(self.points)):
            if len(self.points[i]) >= 2:
                pos = self.points[i][self.tpos[i]]
                r = self.img.GetRed(pos[0], pos[1])
                g = self.img.GetGreen(pos[0], pos[1])
                b = self.img.GetBlue(pos[0], pos[1])
                if self.fxp1[i] != None:
                    self.fxp1[i].setvalR(r)
                    self.fxp2[i].setvalG(g)
                    self.fxp3[i].setvalB(b)
                self.tpos[i] += 1
                if self.tpos[i] >= len(self.points[i]):
                    self.tpos[i] = 0

        self.Refresh()
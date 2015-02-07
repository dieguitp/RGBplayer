import wx, os

class MainPanel(wx.Panel):
    def __init__(self, parent, bg_img='Im.png', size=wx.DefaultSize, fxr=None, fxg=None, fxb=None):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetMinSize(size)
        self.fxr = fxr
        self.fxg = fxg
        self.fxb = fxb
        self.points = []
        self.current = 0
        self.tpos = []
        self.bg = wx.Bitmap(bg_img)
        self.img = wx.Image(bg_img, wx.BITMAP_TYPE_PNG)
        self._width, self._height = self.bg.GetSize()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        
        self.timer = wx.Timer(self)

    def OnEraseBackground(self, evt):
        pass

    def OnLeftDown(self, evt):
        if len(self.points) < 8:
            # une nouvelle traj start le FX
            pos = len(self.points)
            if self.fxr[pos] != None:
                self.fxr[pos].out()
                self.fxg[pos].out()
                self.fxb[pos].out()
            self.points.append([])
            self.tpos.append(0)
            self.points[self.current].append(evt.GetPosition())
            self.CaptureMouse()
            self.Refresh()
        
    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.current += 1
            self.ReleaseMouse()

    def OnMotion(self, evt):
        if self.HasCapture():
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
                dc.DrawLines(self.points[i])
                pos = self.points[i][self.tpos[i]]
                dc.DrawCirclePoint(pos, 10)
                
    def OnTimer(self,evt):
        for i in range(len(self.points)):
            if len(self.points[i]) >= 2:
                pos = self.points[i][self.tpos[i]]
                r = self.img.GetRed(pos[0], pos[1])
                g = self.img.GetGreen(pos[0], pos[1])
                b = self.img.GetBlue(pos[0], pos[1])
                if self.fxr[i] != None:
                    self.fxr[i].setval(r)
                    self.fxg[i].setval(g)
                    self.fxb[i].setval(b)
                self.tpos[i] += 1
                if self.tpos[i] >= len(self.points[i]):
                    self.tpos[i] = 0

        self.Refresh()
import wx, os
from constants import *

class MainPanel(wx.Panel):
    def __init__(self, parent, bg_img='Im.png', size=wx.DefaultSize, fxp=None):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetMinSize(size)
        self.fxp = fxp
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
                self.fxp[i].volume(0)

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
            if self.fxp[pos] != None:
                self.fxp[pos].out()
            self.points.append([])
            self.current = len(self.points) - 1
            self.fxp[self.current].volume(1)
            self.tpos.append(0)
            self.points[self.current].append(evt.GetPosition())
            self.CaptureMouse()
            self.Refresh()
        
    def OnLeftUp(self, evt):
        self.selected = None
        if self.HasCapture():
            self.ReleaseMouse()

    def clip_simple(self, pts):
        w, h = self.GetSize()
        rect = wx.Rect(0, 0, w, h)
        for p in pts:
            if not rect.Contains(p):
                return False
        return True

    def clip_pt(self, pt):
        w, h = self.GetSize()
        if pt[0] < 2:
            pt[0] = 2
        elif pt[0] > w-2:
            pt[0] = w-2
        if pt[1] < 2:
            pt[1] = 2
        elif pt[1] > h-2:
            pt[1] = h-2
        return pt

    def clip(self, diff):
        w, h = self.GetSize()
        min_x, max_x, min_y, max_y = diff[0], diff[0], diff[1], diff[1]
        for pt in self.selectedLine:
            p = pt + diff
            if p[0] < 0:
                min_x = max(min_x, -pt[0])
            elif p[0] > w:
                max_x = min(max_x, w - pt[0])
            if p[1] < 0:
                min_y = max(min_y, -pt[1])
            elif p[1] > h:
                max_y = min(max_y, h - pt[1])
        if diff[0] < 0:
            x = min_x
        else:
            x = max_x
        if diff[1] < 0:
            y = min_y
        else:
            y = max_y
        diff = wx.Point(x, y)
        l = []
        for pt in self.selectedLine:
            l.append(pt + diff)
        return l

    def OnMotion(self, evt):
        if self.HasCapture():
            if self.selected != None:
                pos = evt.GetPosition()
                diff = pos - self.selectedPos
                l = self.clip(diff)
                self.points[self.selected] = l
            else:
                self.points[self.current].append(self.clip_pt(evt.GetPosition()))
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
                if self.fxp[i] != None:
                    self.fxp[i].setvalR(r)
                    self.fxp[i].setvalG(g)
                    self.fxp[i].setvalB(b)
                self.tpos[i] += 1
                if self.tpos[i] >= len(self.points[i]):
                    self.tpos[i] = 0

        self.Refresh()
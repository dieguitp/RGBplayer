import wx
from pyo import *

class Fx:
    def __init__(self,input): #,fxr,fxg,fxb):
        self.input = input
        self.fm = Fm(self.input, ratio1=0.5, ratio2=1.2, index1=1, index2=2).stop()
        self.freqbp = FreqBP(self.input, 0.5).stop()
        self.disto = disto(self.input,0.5).stop()
        self.reverb = reverb(self.input,0.5).stop()
        self.delai = delay(self.input,0.5).stop()
        
        self.curfx = "-- None --"
        self.fx_dict = {'FM': self.fm, 'BP': self.freqbp, 'Distortion': self.disto
        , 'Reverb': self.reverb, 'Delay':self.delai}

    def setval(self, x):
        if self.curfx != "-- None --":
            self.fx_dict[self.curfx].setval(x / 255.)

    def changeFx(self, str):
        go = True
        #if self.curfx != None:
        #    go = self.fx_dict[self.curfx].playing
        #else:
        #    go = False
        if go:
            if self.curfx != "-- None --":
                self.fx_dict[self.curfx].stop()
            if str != "-- None --":
                self.fx_dict[str].out()
        else:
            if str != "-- None --":
                self.fx_dict[str].stop()
        self.curfx = str

    def stop(self):
        if self.curfx != "-- None --":
            self.fx_dict[self.curfx].stop()
        return self

    def out(self):
        if self.curfx != "-- None --":
            self.fx_dict[self.curfx].out()
        return self

class FxBase:
    def __init__(self, input):
        self.input = InputFader(input)
        self.playing = False

    def setInput(self, input, fadetime=0.05):
        self.input.setInput(input, fadetime)

    def setval(self, val):
        self.val.value = val

class Fm:
    def __init__(self, input, ratio1, ratio2, index1, index2):
        self.input = input
        self.yin = Yin(input)
        self.mul = Follower(self.input)
        self.fmod = self.yin * ratio1
        self.fmodmod = self.fmod * ratio2
        self.amod = self.fmod*index1
        self.amodmod = self.fmodmod * index2
        self.modmod = Sine(self.fmodmod, mul=self.amodmod)
        self.mod = Sine(self.fmod+self.modmod, mul=self.amod)
        self.car = Sine(self.yin+self.mod, mul=.2)
        self.eq = EQ(self.car, freq=self.yin, q=0.707, boost=-12)
        self.outo = DCBlock(self.eq,self.mul)
        
    def stop(self):
        self.yin.stop()
        self.mul.stop()
        self.modmod.stop()
        self.mod.stop()
        self.car.stop()
        self.eq.stop()
        self.outo.stop()
        return self
        
    def out(self,out=0):
        self.yin.play()
        self.mul.play()
        self.modmod.play()
        self.mod.play()
        self.car.play()
        self.eq.play()
        self.outo.out(out)
        return self

    def setval(self, val):
        self.val.value = val

class FreqBP(FxBase):
    def __init__(self, input, val):
        FxBase.__init__(self, input)
        self.val = SigTo(val, 0.05, val, mul=4000, add=100)
        self.freq = Resonx(self.input, self.val, q=10)

    def stop(self):
        self.playing = False
        self.freq.stop()
        return self
        
    def out(self,out=0):
        self.playing = True
        self.freq.out(out)
        return self

class disto(FxBase):
    def __init__(self, input, val):
        FxBase.__init__(self, input)
        self.val = SigTo(val, 0.05, val)
        self.dist = Disto(self.input,self.val,mul=.2)
        
    def stop(self):
        self.playing = False
        self.dist.stop()
        return self
        
    def out(self,out=0):
        self.playing = True
        self.dist.out(out)
        return self

class reverb:
    def __init__(self, input, val):
        self.input = input
        self.val = SigTo(val, 0.05, val)
        self.verb = WGVerb(self.input,self.val,5000)
        
    def stop(self):
        self.playing = True
        self.verb.stop()
        return self
        
    def out(self,out=0):
        self.playing = True
        self.verb.out(out)
        return self
        
    def setval(self, val):
        self.val.value = val
        
class delay(FxBase):
    def __init__(self, input, val):
        FxBase.__init__(self, input)
        self.val = SigTo(val, 0.05, val, mul=0.01)
        self.dela = SmoothDelay(self.input,self.val,0.5)
        self.output = Interp(self.input, self.dela, 0.5, mul=0.4)
        
    def stop(self):
        self.playing = True
        self.dela.stop()
        self.output.stop()
        return self
        
    def out(self,out=0):
        self.playing = True
        self.dela.play()
        self.output.out(out)
        return self

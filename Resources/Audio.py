import wx
from pyo import *

class Fx:
    def __init__(self,input): #,fxr,fxg,fxb):
        self.input = input
        self.fm = Fm(self.input, ratio1=0.5, ratio2=1.2, index1=1, index2=2).stop()
        self.freqbp = FreqBP(self.input, 0.5, 0.5, 0.5).stop()
        self.disto = disto(self.input,0.5, 0.5, 0.5).stop()
        self.reverb = reverb(self.input,0.5, 0.5, 0.5).stop()
        self.delai = delay(self.input,0.5, 0.5, 0.5).stop()
        self.ring = Ring(self.input,0.5, 0.5, 0.5).stop()
        self.flanger = Flanger(self.input,0.5, 0.5, 0.5).stop()
        self.vocoder = Voc(self.input,0.5, 0.5, 0.5).stop()

        self.curfx = "-- None --"
        self.fx_dict = {'FM': self.fm, 'BP': self.freqbp, 'Distortion': self.disto
        , 'Reverb': self.reverb, 'Delay':self.delai, 'Ring Modulation':self.ring, 'Flanger':self.flanger,
        'Vocoder':self.vocoder}

    def setvalR(self, x):
        if self.curfx != "-- None --":
            self.fx_dict[self.curfx].setvalR(x / 255.)
            
    def setvalG(self, x):
        if self.curfx != "-- None --":
            self.fx_dict[self.curfx].setvalG(x / 255.)
            
    def setvalB(self, x):
        if self.curfx != "-- None --":
            self.fx_dict[self.curfx].setvalB(x / 255.)

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

    def setvalR(self, valp1):
        self.val1.value = valp1
        
    def setvalG(self, valp2):
        self.val2.value = valp2
        
    def setvalB(self, valp3):
        self.val3.value = valp3
        

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
    def __init__(self, input, valp1, valp2, valp3):
        FxBase.__init__(self, input)
        self.val1 = SigTo(valp1, 0.05, valp1)
        self.sca = Scale(self.val1,outmin=250, outmax=4000, exp = 2)
        self.val2 = SigTo(valp2, 0.05, valp2, mul=10, add=1)
        self.val3 = SigTo(valp3, 0.05, valp3)
        self.f = Resonx(self.input, self.sca, q=self.val2,stages=2)
        self.freq = WGVerb(self.f*self.val3, .95,bal=1)
        self.comp = Compress(self.f+self.freq,ratio=4)
    def stop(self):
        self.playing = False
        self.comp.stop()
        return self
        
    def out(self,out=0):
        self.playing = True
        self.comp.out(out)
        return self

class disto(FxBase):
    def __init__(self, input, valp1, valp2, valp3):
        FxBase.__init__(self, input)
        self.val1 = SigTo(valp1, 0.05, valp1)
        self.amp = Scale(self.val1, outmin=1, outmax=0.1, exp=3)
        self.val2 = SigTo(valp2, 0.09, valp2)
        self.val3 = SigTo(valp2, 0.05, valp2)
        self.cinput = Clip(self.input, min=-0.5, max=0.5, mul=2) 
        self.dist = Disto(self.cinput, self.val1, self.val2, mul=self.amp)
        self.bit = self.val2 * 6 + 4
        self.dcut = Scale(self.val2, outmin=4000, outmax=15000, exp=3)
        self.srs = self.val3 * 0.35 + 0.1
        self.deg = Degrade(self.cinput, self.bit, self.srs)
        self.dlp = ButLP(self.deg, self.dcut)
        self.output = Interp(self.dist, self.dlp, 0.5)

    def stop(self):
        self.playing = False
        self.output.stop()
        return self
        
    def out(self,out=0):
        self.playing = True
        self.output.out(out)
        return self

class reverb(FxBase):
    def __init__(self, input, valp1, valp2, valp3):
        FxBase.__init__(self, input)
        self.val1 = SigTo(valp1, 0.25, valp1)
        self.val2 = SigTo(valp1, 0.05, valp1)
        self.val3 = SigTo(valp1, 0.05, valp1)
        self.dtime = self.val2 * 0.9 + 0.1
        self.delay = SmoothDelay(self.input, delay=self.dtime, feedback=self.val3, mul=self.val3)
        self.feed = Scale(self.val1, outmin=0.1, outmax=10, exp=4)
        self.cut = Scale(self.val1, outmin=10000, outmax=1000, exp=4)
        self.verb = STRev(self.input+self.delay, inpos=0.5, revtime=self.feed, cutoff=self.cut, bal=0.5)
        
    def stop(self):
        self.playing = False
        self.delay.stop()
        self.feed.stop()
        self.cut.stop()
        self.verb.stop()
        return self
        
    def out(self,out=0):
        self.playing = True
        self.delay.play()
        self.feed.play()
        self.cut.play()
        self.verb.out(out)
        return self
        

class delay(FxBase):
    def __init__(self, input, valp1, valp2, valp3):
        FxBase.__init__(self, input)
        self.val1 = SigTo(valp1, 0.05, valp1, mul=0.01)
        self.val2 = SigTo(valp2, 0.05, valp2, mul=0.01)
        self.val3 = SigTo(valp1, 0.05, valp1)
        self.dela = SmoothDelay(self.input, self.val1, self.val2)
        self.output = Interp(self.input, self.dela, 0.5, mul=0.4)
        
    def stop(self):
        self.playing = False
        self.dela.stop()
        self.output.stop()
        return self
        
    def out(self,out=0):
        self.playing = True
        self.dela.play()
        self.output.out(out)
        return self

class Ring(FxBase):
    def __init__(self, input, valp1, valp2, valp3):
        FxBase.__init__(self, input)
        self.val1 = SigTo(valp1, 0.05, valp1)
        self.val2 = SigTo(valp2, 0.05, valp2)
        self.val3 = SigTo(valp3, 0.05, valp3)
        self.sca1 = Scale(self.val1, outmin=1, outmax=1000)
        self.sca2 = Scale(self.val2, outmin=1, outmax=1000)
        self.sca3 = Scale(self.val3, outmin=1, outmax=1000)

        self.mod1 = Sine(self.sca1,mul=self.input)
        self.mod2 = Sine(self.sca2,mul=self.input)
        self.mod3 = Sine(self.sca3,mul=self.input)
        self.gain = self.mod1 + self.mod2 + self.mod3

        
    def stop(self):
        self.playing = False
        self.gain.stop()
        return self
        
    def out(self,out=0):
        self.playing = True
        self.gain.out(out)
        return self
        
class Flanger(FxBase):
    def __init__(self, input, valp1, valp2, valp3):
        FxBase.__init__(self, input)
        self.val1 = SigTo(valp1, 0.05, valp1)
        self.val2 = SigTo(valp2, 0.05, valp2)
        self.val3 = SigTo(valp3, 0.05, valp3)
        self.lfo = Sine(self.val1, mul=self.val2*0.005, add=0.005)
        self.flan = Delay(self.input, self.lfo, feedback=self.val3, add=self.input)
        
    def stop(self):
        self.playing = False
        self.flan.stop()
        return self
        
    def out(self,out=0):
        self.playing = True
        self.flan.out(out)
        return self
        
class Voc(FxBase):
    def __init__(self, input, valp1, valp2, valp3):
        FxBase.__init__(self, input)
        self.val1 = SigTo(valp1, 0.05, valp1)
        self.val2 = SigTo(valp2, 0.05, valp2)
        self.val3 = SigTo(valp3, 0.05, valp3)
        self.noise = PinkNoise()
        self.voc = Vocoder(self.input,self.noise)
        
    def stop(self):
        self.playing = False
        self.voc.stop()
        return self
        
    def out(self,out=0):
        self.playing = True
        self.voc.out(out)
        return self

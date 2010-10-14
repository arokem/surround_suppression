
import numpy as np
from psychopy import visual,core,event
import psychopy.monitors.calibTools as calib

from ss_tools import *
from ss_classes import Params,Text

rgb = np.array([1.,1.,1.])
two_pi = 2*np.pi


#Read a params object from the localizer params file:
p = Params(p_file='localizer_params')
ss_p = Params(p_file='ss_params')

calib.monitorFolder = './calibration/'# over-ride the usual setting of where
                                      # monitors are stored

mon = calib.Monitor(p.monitor) #Get the monitor object and pass that as an
                                    #argument to win:

win = visual.Window(monitor=mon,units='deg',
              screen=p.screen_number,
              fullscr=p.full_screen)

annulus = visual.RadialStim(win,size=ss_p.annulus_outer,
                            radialCycles=p.radial_cyc,
                            angularCycles=p.angular_cyc)
annulus.setSF = p.sf

fixation = visual.PatchStim(win, tex=None, mask = 'circle',color=1*rgb,
                                size=p.fixation_size)

fixation_surround = visual.PatchStim(win, tex=None, mask='circle',
                                         color=-1*rgb,
                                         size=p.fixation_size*1.5)

inner_gray = visual.PatchStim(win,tex=None,mask='circle',color=0*rgb,
                              size = ss_p.annulus_inner)

inner_surround = visual.RadialStim(win,size=ss_p.annulus_inner,
                            radialCycles=p.radial_cyc,
                            angularCycles=p.angular_cyc)
inner_surround.setSF = p.sf

outer_surround = visual.RadialStim(win,size=p.size,
                            radialCycles=p.radial_cyc,
                            angularCycles=p.angular_cyc)
outer_surround.setSF = p.sf

annulus_gray = visual.PatchStim(win,tex=None,mask='circle',color=0*rgb,
                              size = ss_p.annulus_outer)

message = """READY? \n Press a key and then be ready to FIXATE!"""
#Initialize and call in one:
Text(win,text=message,height=0.5)() 

if p.scanner:
    core.wait(1)
    Text(win,text='',height=0.5)() 

# Initialize to True:
switcheroo = True
r_phase_sign = np.sign(np.random.randn(1))
a_phase_sign = np.sign(np.random.randn(1))
t_arr = []

for block in xrange(p.n_blocks):
    block_clock = core.Clock()
    t=0
    t_previous = 0
    while t<p.block_duration:
        t = block_clock.getTime()
        t_diff = t-t_previous 

        #Annulus block:
        if np.mod(block,2)==0:

            if t>1 and np.mod(int(t),2)==0:
                if switcheroo:
                    r_phase_sign = np.sign(np.random.randn(1))
                    a_phase_sign = np.sign(np.random.randn(1))
                    switcheroo = False

            if np.mod(int(t)-1,2)==0:
                switcheroo = True

            #The contrast just reverses (no randomness)
            annulus.setContrast(np.sin(t*p.temporal_freq*np.pi*2))

            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break

            annulus.setRadialPhase(annulus.radialPhase +
                                   r_phase_sign*t_diff*two_pi/p.temporal_freq)

            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break
            annulus.setAngularPhase(annulus.angularPhase  +
                                   a_phase_sign*t_diff*two_pi/p.temporal_freq)


            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break
            annulus.draw()
            inner_gray.draw()

        else:
            if t>1 and np.mod(int(t),2)==0:
                if switcheroo:
                    r_phase_sign = np.sign(np.random.randn(1))
                    a_phase_sign = np.sign(np.random.randn(1))
                    switcheroo = False

            if np.mod(int(t)-1,2)==0:
                switcheroo = True

            #The contrast just reverses (no randomness)
            outer_surround.setContrast(np.sin(t*p.temporal_freq*np.pi*2))
            inner_surround.setContrast(np.sin(t*p.temporal_freq*np.pi*2))

            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break

            outer_surround.setRadialPhase(outer_surround.radialPhase +
                                   r_phase_sign*t_diff*two_pi/p.temporal_freq)
            inner_surround.setRadialPhase(inner_surround.radialPhase +
                                   r_phase_sign*t_diff*two_pi/p.temporal_freq)

            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break
            outer_surround.setAngularPhase(outer_surround.angularPhase  +
                                   a_phase_sign*t_diff*two_pi/p.temporal_freq)
            inner_surround.setAngularPhase(inner_surround.angularPhase  +
                                   a_phase_sign*t_diff*two_pi/p.temporal_freq)


            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break
            
            outer_surround.draw()
            annulus_gray.draw()
            inner_surround.draw()
            
            
        #Keep checking for time:
        if block_clock.getTime()>=p.block_duration:
            break
        fixation_surround.draw()

        #Keep checking for time:
        if block_clock.getTime()>=p.block_duration:
            break
        fixation.draw()
        
        #Keep checking for time:
        if block_clock.getTime()>=p.block_duration:
            break
        win.flip()

        #Keep checking for time:
        if block_clock.getTime()>=p.block_duration:
            break

        #handle key presses each frame
        for key in event.getKeys():
            if key in ['escape','q']:
                win.close()
                core.quit()

        t_previous = t
        t_arr.append(block_clock.getTime())

print(np.max(t_arr))
win.close()
core.quit()

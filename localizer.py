
import numpy as np
from psychopy import visual,core,event
import psychopy.monitors.calibTools as calib

from tools import *

rgb = np.array([1.,1.,1.])
two_pi = 2*np.pi


#Read a params object from the localizer params file:
p = Params(p_file='localizer_params')

calib.monitorFolder = './calibration/'# over-ride the usual setting of where
                                      # monitors are stored

mon = calib.Monitor(p.monitor) #Get the monitor object and pass that as an
                                    #argument to win:

win = visual.Window(monitor=mon,units='deg',
              screen=p.screen_number,
              fullscr=p.full_screen)

c_board = visual.RadialStim(win,size=p.size,radialCycles=p.radial_cyc,
                            angularCycles=p.angular_cyc)
c_board.setSF = p.sf

fixation = visual.PatchStim(win, tex=None, mask = 'circle',color=1*rgb,
                                size=p.fixation_size)

fixation_surround = visual.PatchStim(win, tex=None, mask='circle',
                                         color=-1*rgb,
                                         size=p.fixation_size*1.5)



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

        if np.mod(block,2)==0:
            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break

            fixation_surround.setColor(-1*rgb)

            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break
            
            fixation.setColor(1*rgb)

            if t>1 and np.mod(int(t),2)==0:
                if switcheroo:
                    r_phase_sign = np.sign(np.random.randn(1))
                    a_phase_sign = np.sign(np.random.randn(1))
                    switcheroo = False

            if np.mod(int(t)-1,2)==0:
                switcheroo = True

            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break

            #The contrast just reverses (no randomness)
            c_board.setContrast(np.sin(t*p.temporal_freq*np.pi*2))

            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break
            c_board.setRadialPhase(c_board.radialPhase +
                                   r_phase_sign*t_diff*two_pi/p.temporal_freq)

            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break
            c_board.setAngularPhase(c_board.angularPhase  +
                                   a_phase_sign*t_diff*two_pi/p.temporal_freq)


            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break
            c_board.draw()

        else:
            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break
            fixation_surround.setColor(-1*np.sin(t*p.temporal_freq*np.pi*2)*rgb)

            #Keep checking for time:
            if block_clock.getTime()>=p.block_duration:
                break
            fixation.setColor(np.sin(t*p.temporal_freq*np.pi*2)*rgb)
            
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

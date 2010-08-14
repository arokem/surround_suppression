"""

Meant as a place to try generating the stimuli and playing around with them

"""
import numpy as np
from psychopy import visual,core

#For now, set these params locally, eventually move to the params file: 

duration = 10

#For the grating:
temporal_freq = 4
spatial_freq = 1.1

surround_ori = 0
annulus_ori = 90

surround_contrast = 1.
annulus_contrast = 0.5

surround_outer = 12.2
annulus_outer = 6
annulus_inner = 3
surround_inner = 0.4

ring_width = 0.1
spoke_width = 0.1

win = visual.Window((600,600.0),
                    allowGUI=False,
                    monitor='testMonitor',
                    units='deg')

outer_surround  = visual.PatchStim(win,tex="sin",mask="circle",texRes=128,
                                   color=[1.0,1.0,1.0],
                                   colorSpace='rgb', opacity=1.0,
                                   contrast = surround_contrast,
                                   size=(surround_outer-ring_width/2,
                                         surround_outer-ring_width/2),
                                   sf=(spatial_freq,spatial_freq),
                                   ori = surround_ori)

annulus = visual.PatchStim(win,tex="sin",mask="circle",texRes=128,
                           color=annulus_contrast,
                           colorSpace='rgb',
                           opacity=1.0,
                           size=(annulus_outer-ring_width/2,
                                 annulus_outer-ring_width/2),
                           sf=(spatial_freq,spatial_freq),
                           ori = annulus_ori)

inner_surround = visual.PatchStim(win,tex="sin",mask="circle",texRes=128,
                                  color=[1.0,1.0,1.0],
                                  colorSpace='rgb',
                                  opacity=1.0,
                                  contrast=surround_contrast,
                                  size=(annulus_inner-ring_width/2,
                                        annulus_inner-ring_width/2),
                                  sf=(spatial_freq,spatial_freq),
                                  ori = surround_ori)

#This is the bit between the annulus and the outer surround: 
ring1 = visual.RadialStim(win, tex=None, color=[-1,-1,-1],
                          size=[annulus_outer+ring_width/2,
                               annulus_outer+ring_width/2],
                          units='deg',
                          visibleWedge=[0, 360],
                          radialCycles=4, angularCycles=8,
                          interpolate=True,contrast = 1)

#This is the bit between the annulus and the inner surround: 
ring2 = visual.RadialStim(win, tex=None, color=[-1,-1,-1],
                          size=[annulus_inner+ring_width/2,
                                annulus_inner+ring_width/2],
                          units='deg',
                          visibleWedge=[0, 360],
                          radialCycles=4, angularCycles=8,
                          interpolate=True,contrast = 1)

#This is the central area, between the inner surround and the fixation: 
center_area = visual.RadialStim(win, tex=None, color=0,
                          size=[surround_inner,
                                surround_inner],
                          units='deg',
                          visibleWedge=[0, 360],
                          radialCycles=4, angularCycles=8,
                          interpolate=True,contrast = 1)


target_wedge = visual.RadialStim(win, tex = None, color=0,
                                 opacity = 0.5,
                                 size = [annulus_outer,annulus_outer],
                                 visibleWedge=[0, 45],
                                 ) 
#fixation = visual.RadialStim(win,tex ='sin' fixation_tex)

#Setting the tex argument to None sets this to just be uniform: 
center = visual.PatchStim(win,tex=None) 

trial_clock = core.Clock()
t = lastFPSupdate = 0

while t<duration:#sets the duration
    t=trial_clock.getTime()
    annulus.setContrast(np.sin(t*temporal_freq*np.pi*2))
    inner_surround.setContrast(np.sin(t*temporal_freq*np.pi*2))    
    outer_surround.setContrast(np.sin(t*temporal_freq*np.pi*2))    

    #Draw them (order matters!)
    outer_surround.draw()
    ring1.draw()
    annulus.draw()  
    ring2.draw()
    target_wedge.draw()
    inner_surround.draw()
    center_area.draw()
    
    win.flip() #update the screen

win.close()

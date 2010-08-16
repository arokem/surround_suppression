"""

Meant as a place to try generating the stimuli and playing around with them

"""
import numpy as np
from psychopy import visual,core

#For now, set these params locally, eventually move to the params file: 

duration = 5

#For the grating:
temporal_freq = 4
spatial_freq = 1.1

surround_ori = 0
annulus_ori = 90

surround_contrast = 1.
annulus_contrast = 0.8
target_contrast = 0.1

surround_outer = 12.2
annulus_outer = 6
annulus_inner = 3
surround_inner = 0.4

fixation_size = 0.2

ring_width = 0.1
spoke_width = 0.1
num_spokes = 8

target_loc = 4

win = visual.Window((800,800),
                    allowGUI=False,
                    monitor='testMonitor',
                    units='deg')
    

outer_surround  = visual.PatchStim(win,tex="sin",mask="circle",texRes=256,
                                   color=surround_contrast,
                                   size=(surround_outer-ring_width/2,
                                         surround_outer-ring_width/2),
                                   sf=(spatial_freq,spatial_freq),
                                   ori = surround_ori)

annulus = visual.PatchStim(win,tex="sin",mask="circle",texRes=256,
                           color=annulus_contrast,
                           size=(annulus_outer-ring_width/2,
                                 annulus_outer-ring_width/2),
                           sf=(spatial_freq,spatial_freq),
                           ori = annulus_ori)

inner_surround = visual.PatchStim(win,tex="sin",mask="circle",texRes=256,
                                  color=surround_contrast,
                                  size=(annulus_inner-ring_width/2,
                                        annulus_inner-ring_width/2),
                                  sf=(spatial_freq,spatial_freq),
                                  ori = surround_ori)

#This is the bit between the annulus and the outer surround: 
ring1 = visual.PatchStim(win, tex=None, mask='circle', color=-1,
                          size=[annulus_outer+ring_width/2,
                               annulus_outer+ring_width/2],
                         interpolate=True)

#This is the bit between the annulus and the inner surround: 
ring2 = visual.PatchStim(win, tex=None, mask='circle', color=-1,
                          size=[annulus_inner+ring_width/2,
                                annulus_inner+ring_width/2],
                          interpolate=True)

#This is the central area, between the inner surround and the fixation: 
center_area = visual.PatchStim(win, tex=None, mask='circle', color=0,
                          size=[surround_inner,
                                surround_inner],
                          interpolate=True)

#Generate a mask, which will cover everything except for the target wedge:
grid_array = np.linspace(-1*annulus.size[0],annulus.size[0],annulus.texRes)
x,y=np.meshgrid(grid_array,grid_array)
r = np.sqrt(x**2 + y**2)
theta = np.arctan2(x,y) + np.pi
target_mask = np.ones((annulus.texRes,annulus.texRes))
target_mask[np.where(r>annulus_outer)] = -1
target_mask[np.where(r<annulus_inner)] = -1
target_mask[np.where(theta<target_loc*np.deg2rad(45))] = -1
target_mask[np.where(theta>(target_loc+1)*np.deg2rad(45))]=-1

#Now show the target contrast in the wedge:
target_wedge = visual.PatchStim(win,tex="sin",mask=target_mask,
                                texRes=256,
                                color=target_contrast,
                                size=(annulus_outer-ring_width/2,
                                annulus_outer-ring_width/2),
                                sf=(spatial_freq,spatial_freq),
                                ori = annulus_ori)

spokes = []
for i in np.arange(num_spokes/2):
    spokes.append(visual.ShapeStim(win,
                         fillRGB = -1,
                         lineRGB = -1,
                         vertices = ((-spoke_width/2,annulus_outer/2),
                                     (spoke_width/2,-annulus_outer/2),
                                     (-spoke_width/2,-annulus_outer/2),
                                     (spoke_width/2,annulus_outer/2)),
                         ori=i*45))

# Fixation (made out of two concentric squares):
fixation = visual.PatchStim(win, tex=None, color=1,
                            size=fixation_size,
                            interpolate=True)

fixation_center = visual.PatchStim(win, tex=None, color=-1,
                            size=fixation_size/2,
                            interpolate=True)

trial_clock = core.Clock()
t = lastFPSupdate = 0

while t<duration:#sets the duration
    t=trial_clock.getTime()
    annulus.setContrast(np.sin(t*temporal_freq*np.pi*2))
    inner_surround.setContrast(np.sin(t*temporal_freq*np.pi*2))    
    outer_surround.setContrast(np.sin(t*temporal_freq*np.pi*2))    
    target_wedge.setContrast(np.sin(t*temporal_freq*np.pi*2))

    #Draw them (order matters!)
    outer_surround.draw()
    ring1.draw()
    annulus.draw()  
    target_wedge.draw()
    for spoke in spokes:
        spoke.draw()
    ring2.draw()
    inner_surround.draw()
    center_area.draw()
    fixation.draw()
    fixation_center.draw()

    win.flip() #update the screen

win.close()

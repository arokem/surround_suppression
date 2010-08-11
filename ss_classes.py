"""Base classes for the surround suppression experiment

- Stimulus
- Staircase
- Trial

""" 

import numpy as np
from psychopy import core, visual, event

params = dict()

class Staircase(object):
    """
    This is an object for holding, updating and potentially analyzing
    A psychophysical staircase

    """ 
    def __init__(self,start,step,n_up=3,n_down=1,harder=-1,ub=1,lb=0):
        """
        Initialization function for the staircase class

        Parameters
        ----------
        start: The starting value of the staircase
        step: The size of the step used when updating the staircase
        n_up,n_down: The kind of staircase to be used, defaults to a 3-up,
                     1-down staircase 

        harder: {-1,1} The direction which would make the task harder. Defaults to -1,
        which is true for the contrast decrement detection task.  

        """
        self.value = start
        self.n_up = n_up
        self.step = step
        self.n = 0 #This is what will be compared to n_up for udpating.
        self.harder = np.sign(harder) #Make sure that this is only -1 or 1.
        
    def update(self,correct):
        """

        This function updates the staircase value, accroding to the state of
        the staircase, the n/n_up values and whether or not the subject got it
        right. This staircase is then propagated on to the next trial.

        Parameters
        ----------
        correct: {True|False} 

        """

        if correct:
            if self.n>=self.n_up:
                self.value += self.harder * self.step #'harder' sets the sign
                                                      #of the change to make it
                                                      #harder
                self.n = 0
            else:
                self.n +=1
                
        else:
            self.n = 0
            self.value -= self.harder * self.step #Change in the
                                        #opposite direction than above to make
                                        #it easier!


class Stimulus(object):
    """
    This is the stimulus object for the 
    

    In order to generate counter-phase, we vary the contrast of the grating
    between -1 and 1, according to the frequency


    """

    def __init__(win,):
    
    self.grating = visual.PatchStim(win,tex="sin",mask="circle",texRes=128,
            color=[1.0,1.0,1.0],colorSpace='rgb', opacity=1.0,
            size=(5.0,5.0), sf=(2.0,2.0),
            ori = 45, depth=0.5)

    #Setting the tex argument to None sets this to just be uniform: 
    self.center = visual.PatchStim(win,tex=None) 
    
    trial_clock = core.Clock()
    t = lastFPSupdate = 0

    def show():
        while t<duration:#sets the duration
            t=trial_clock.getTime()

            self.grating.setContrast(sin(t*pi*2))
            self.grating.draw()  #redraw it

            win.flip()          #update the screen


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
        self.record = [start]
        
    def update(self,correct):
        """

        This function updates the staircase value, according to the state of
        the staircase, the n/n_up values and whether or not the subject got it
        right. This staircase is then propagated on to the next trial.

        Parameters
        ----------
        correct: {True|False} 

        """

        if correct:
            if self.n>=self.n_up-1:
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

        #Add to the records the updated value: 
        self.record.append(self.value)
    

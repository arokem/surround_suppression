"""

Surround suppression experiment, based on Zenger-Landolt and Heeger (2003)

And on the Psychtoolbox version used to get the data in Yoon et al. (2009 and
2010).

""" 

import numpy as np
from ss_classes import Params
from psychopy import gui

#This brings in all of the classes defined in ss_classes:
from ss_classes import *

if __name__ == "__main__":
    """ The main function. This actually runs the experiment """

    #Initialize params from file:
    params = Params()
    params.set_by_gui(subject_id = '', condition = 'ortho')

    if params.condition == 'ortho':
        params.annulus_ori = params.surround_ori + 90
    else:
        params.annulus_ori = params.surround_ori
        
    #After this is done, info now has in it what the user put in there.

    #This initializes the window (for now, this is just a part of monitor 0):
    win = visual.Window([800,600],allowGUI=True)

    #Compile a list of events
    #XXX TODO
        
    #Loop over this list, while consuming each event, by calling it:
    
##     for this_event in event_list:
        
##         this_event.finalize(inputs) #What needs to be provided as input 
##         result = this_event(other_inputs) #The __call__ method makes the event
##                                         #actually happen

##         #Record the result of this event somehow and pass it on to the next
##         #event in the line. Maybe update the staircase at this point? 

    win.close()

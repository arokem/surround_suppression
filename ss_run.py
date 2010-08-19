"""

Surround suppression experiment, based on Zenger-Landolt and Heeger (2003)

And on the Psychtoolbox version used to get the data in Yoon et al. (2009 and
2010).

""" 

import numpy as np

from psychopy import gui

#This brings in all of the classes defined in ss_classes:
from ss_classes import *

if __name__ == "__main__":
    """ The main function. This actually runs the experiment """

    #Initialize params from file:

    params = params
    
    info = dict(id='',condition='')  #This initializes the information that
                                     #needs to be set through a gui

    #This allows the user to update the information in the dict:
    gui = gui.DlgFromDict(dictionary=info,title='Enter run info')

    #After this is done, info now has in it what the user put in there.

    #This initializes the window (for now, this is just a part of monitor 0):
    win = visual.Window([800,600],allowGUI=True)

    #Compile a list of events
    
    

    for this_event in event_list:
        
        this_event.finalize(inputs) #What needs to be provided as input 
        result = this_event(other_inputs) #The __call__ method makes the event
                                        #actually happen

        #Record the result of this event somehow and pass it on to the next
        #event in the line. Maybe update the staircase at this point? 


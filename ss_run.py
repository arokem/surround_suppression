"""This actually runs the experiment """ 


import numpy as np
from psychopy import gui



if __name__ == "__main__":
    """ The main function"""

    #Initialize params from file
    

    
    
    info = dict(id='',condition='')  #This initializes the information that
                                     #needs to be set through a gui

    #This allows the user to update the information in the dict:
    gui = gui.DlgFromDict(dictionary=info,title='Enter run info')

    #After this is done, info now has in it what the user put in there.

    #This initializes the window (for now, this is just a part of monitor 0):
    win = visual.Window([800,600],allowGUI=True)

    #Compile a list of events
    
    

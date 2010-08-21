"""

Surround suppression experiment, based on Zenger-Landolt and Heeger (2003)

And on the Psychtoolbox version used to get the data in Yoon et al. (2009 and
2010).

""" 
import wx
import numpy as np
from ss_classes import Params
from psychopy import gui


#This brings in all of the classes defined in ss_classes:
from ss_classes import *
    
if __name__ == "__main__":
    """ The main function. This actually runs the experiment """

    #Initialize params from file:
    params = Params()
    #For some reason, if this call is inside ss_classes, just importing
    #ss_classes starts an instance of the GUI, so we put it out here:
    app = wx.App()
    params.set_by_gui()
    app.MainLoop()
    params.target_ori = params.annulus_ori
    
    #This initializes the window (for now, this is just a part of monitor 0):
    win = visual.Window([800,600],monitor='testMonitor',units='deg')

    staircase = Staircase(params.start_target_contrast,
                          params.annulus_contrast/params.contrast_increments)

    trial_list = [Trial(win,params,0),Trial(win,params,1),Trial(win,params,2)]

    #Send a message to the screen and wait for a subject keypress:
    start_text(win) 
        
    #Loop over the event list, while consuming each event, by calling it:
    
    for this_trial in trial_list:
        #
        this_trial.stimulus.finalize(params,target_co=staircase.value,
                                     target_loc=0)
        this_trial.stimulus(duration=params.stimulus_duration)
        this_trial.fixation(duration=0.01) 
        this_trial.response.finalize(correct_key = '1')
        correct = this_trial.response()
        this_trial.feedback.finalize(correct)
        this_trial.feedback()
        staircase.update(correct)

    win.close()

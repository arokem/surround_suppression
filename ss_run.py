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
    app.MainLoop()
    params.set_by_gui()
    params.target_ori = params.annulus_ori
    
    #This initializes the window (for now, this is just a part of monitor 0):
    win = visual.Window([800,600],monitor='testMonitor',units='deg')

    #Make a trial list:
    trial_list = [Trial(win,params,0),Trial(win,params,1),Trial(win,params,2)]

    #Initialize the staircase, depending on which task is performed
    if params.task == 'Annulus':
        staircase = Staircase(params.start_target_contrast,
                            params.annulus_contrast/params.contrast_increments,
                            harder = 1, #For this task, higher values are
                                      #actually harder => closer to the annulus
                                      #value
                            ub=params.target_contrast_max,
                            lb=params.target_contrast_min
                            )
        fix_target_co = np.ones(len(trial_list)) * params.fix_target_start
    
    elif params.task == 'Fixation':
        staircase = Staircase(params.fix_target_start,
                            params._contrast/params.contrast_increments,
                            harder = 1, 
                            ub=params.fix_target_max,
                            lb=params.fix_target_min
                            )
        target_co = np.ones(len(trial_list)) * params.start_target_contrast
        

    #Send a message to the screen and wait for a subject keypress:
    start_text(win) 
        
    #Loop over the event list, while consuming each event, by calling it:
    for trial_idx,this_trial in enumerate(trial_list):
        if params.task=='Annulus':
            this_trial.stimulus.finalize(params,target_co=staircase.value,
                                         target_loc=0,fix_target_loc=1,
                                         fix_target_co=fix_target_co[trial_idx])

        elif params.task=='Fixation':
            this_trial.stimulus.finalize(params,target_co=target_co[trial_idx],
                                         target_loc=0,fix_target_loc=1,
                                         fix_target_co=staircase.value)

        this_trial.stimulus()
        this_trial.fixation()

        
        this_trial.response.finalize(correct_key = '1')
        correct = this_trial.response()

        this_trial.feedback.finalize(correct)
        this_trial.feedback()

        staircase.update(correct)

    win.close()
    

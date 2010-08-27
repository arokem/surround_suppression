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
from ss_tools import start_data_file
    
if __name__ == "__main__":
    """ The main function. This actually runs the experiment """

    #Initialize params from file:
    params = Params()
    #For some reason, if this call is inside ss_classes, just importing
    #ss_classes starts an instance of the GUI, so we put it out here:
    app = wx.App()
    app.MainLoop()
    params.set_by_gui()

    f = start_data_file(params.subject)

    #Start by saving in the parameter setting:
    params.save(f)
    
    #For now, assume that the target and the annulus are going to have the same
    #orientation: 
    params.target_ori = params.annulus_ori
    
    #This initializes the window (for now, this is just a part of monitor 0):
    win = visual.Window(params.window_res,
                        monitor=params.monitor,
                        units=params.display_units)

    #Make a trial list:
    trial_list = [Trial(win,params,0,1),Trial(win,params,1,0),
                  Trial(win,params,2,1),Trial(win,params,3,1),
                  Trial(win,params,4,0),Trial(win,params,5,1),
                  Trial(win,params,6,0),Trial(win,params,7,1)]

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
        #The fixation target appears but has a constant contrast set to the
        #starting point 
        fix_target_co = np.ones(len(trial_list)) * params.fix_target_start
    
    elif params.task == 'Fixation':
        staircase = Staircase(params.fix_target_start,
                            params.fix_target_start/params.contrast_increments,
                            harder = 1, 
                            ub=params.fix_target_max,
                            lb=params.fix_target_min
                            )
        #The annulus target appears, but has a constant contrast set to the
        #start contrast:
        target_co = np.ones(len(trial_list)) * params.start_target_contrast
        

    #Send a message to the screen and wait for a subject keypress:
    start_text(win) 
        
    #Loop over the event list, while consuming each event, by calling it:
    for trial_idx,this_trial in enumerate(trial_list):

        #Preparing the stimulus depends on which task we are doing:
        if params.task=='Annulus':
            this_trial.stimulus.finalize(params,target_co=staircase.value,
                                    target_loc=this_trial.target_loc,
                                    fix_target_loc=this_trial.fix_target_loc,
                                    fix_target_co=fix_target_co[trial_idx])
            if this_trial.target_loc in [0,1,2,3]:
                correct_key = '1'
            else:
                correct_key = '2'

        elif params.task=='Fixation':
            this_trial.stimulus.finalize(params,target_co=target_co[trial_idx],
                                    target_loc=this_trial.target_loc,
                                    fix_target_loc=this_trial.fix_target_loc,
                                    fix_target_co=staircase.value)
            if this_trial.fix_target_loc == 1:
                correct_key = '2'
            else:
                correct_key = '1'
            
        this_trial.stimulus()

        #Doesn't need finalizing:
        this_trial.fixation()
        
        this_trial.response.finalize(correct_key = correct_key)
        this_trial.response()

        this_trial.feedback.finalize(this_trial.response.correct)
        this_trial.feedback()

        staircase.update(this_trial.response.correct)

        if trial_idx == 0:
            #On the first trial, insert the header: 
            f = this_trial.save(f,insert_header=True)
        else:
            #On other trials, just insert the data:
            f = this_trial.save(f)

        this_trial.wait_iti()

    f.close()
    win.close()
    

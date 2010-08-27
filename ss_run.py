"""

Surround suppression experiment, based on Zenger-Landolt and Heeger (2003)

And on the Psychtoolbox version used to get the data in Yoon et al. (2009 and
2010).

""" 
import wx
import numpy as np
from ss_classes import Params
from psychopy import core

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
    trial_list = make_trial_list(win,params)

    #Initialize the staircase, depending on which task is performed
    if params.task == 'Annulus':
        message = """ On which side are the targets in the GRATING?\n Press 1 for left and 2 for right\n Press any key to start""" 
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
        other_contrast = np.ones(len(trial_list)) * params.fix_target_start
    
    elif params.task == 'Fixation':
        message = """ On which side are the targets in the FIXATION?\n Press 1 for left and 2 for right\n Press any key to start"""
        
        staircase = Staircase(params.fix_target_start,
                            params.fix_target_start/params.contrast_increments,
                            harder = 1, 
                            ub=params.fix_target_max,
                            lb=params.fix_target_min
                            )
        #The annulus target appears, but has a constant contrast set to the
        #start contrast:
        other_contrast = np.ones(len(trial_list)) * params.start_target_contrast
        

    #Send a message to the screen and wait for a subject keypress:
    Text(win,text=message,height=0.7)() 

    #If this is in the scanner, we would want to wait for the ttl pulse right
    #here:
    #if params.monitor == 'scanner':
    #    start_text(win,text='',keys=['5']) #Assuming a TTL is a '5' key
    
    #Loop over the event list, while consuming each event, by calling it:
    for trial_idx,this_trial in enumerate(trial_list):

        this_trial.finalize(staircase,other_contrast[trial_idx])            
        this_trial.stimulus()

        #Doesn't need finalizing:
        this_trial.fixation()

        #We pass the file to the response, so that the file can be cleanly
        #closed in case of quitting:
        this_trial.response.finalize(correct_key = this_trial.correct_key,
                                     file_name=f)
        this_trial.response()

        #Finalize the feedback in cases a correct_key was defined (on trials on
        #which some response was expected):
        if this_trial.correct_key is not None:
            this_trial.feedback.finalize(this_trial.response.correct)

        #This will do something only in cases in which there was a task:
        this_trial.feedback()

        #Update and save only on trials in which there was a target:
        if this_trial.target_loc is not None:
            if len(staircase.record)==1:
               #On the first trial, insert the header: 
               f = this_trial.save(f,insert_header=True)
            else:
               #On other trials, just insert the data:
               f = this_trial.save(f)
            #update after saving:
            staircase.update(this_trial.response.correct)

        this_trial.wait_iti()

    f.close()
    core.quit()
    

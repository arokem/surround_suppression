import sys

from psychopy import gui
from matplotlib.mlab import csv2rec
import matplotlib.pyplot as plt
import numpy as np
import wx

#from pypsignifit import (BootstrapInference,GoodnessOfFit,ParameterPlot,
#                         ThresholdPlot)

myDlg = gui.Dlg(title="Gui for Data Analysis")#Create a dialog box with title "Gui for Data analysis"
myDlg.addText('Data File')#title of dialog box
myDlg.addField('File:')#adds the field to let user input file name
myDlg.show()#show dialog box
if gui.OK:
    file_name = str(myDlg.data)
    file_name = 'data/' + file_name[3:-2] #takes the 4th to 3rd to last letter to remove messy bits put in by myDlg
    print file_name
else:
    print 'user cancelled'
contrast = []

if __name__=="__main__":
    file_read = file(file_name,'r')
    p = {} #This will hold the params
    l = file_read.readline()
    
    while l[0]=='#':
        try:
            p[l[1:l.find(':')-1]]=float(l[l.find(':')+1:l.find('\n')]) 

        #Not all the parameters can be cast as float (the task and the subject)
        except:
            p[l[2:l.find(':')-1]]=l[l.find(':')+1:l.find('\n')]
            
        l = file_read.readline()
    data_rec = csv2rec(file_name)
    annulus_target_contrast = data_rec['annulus_target_contrast']
    correct = data_rec['correct']
    #Which staircase to analyze:
    if p['task'] == ' Fixation ':
        contrast = 1-data_rec['fixation_target_contrast']
        hit_amps = contrast[correct==1]
        miss_amps = contrast[correct==0]
    elif p['task']== ' Annulus ':
        #if data_rec['annulus_target_contrast'] >= 0.75#params.targetA_contrast_min
        contrast_all = data_rec['annulus_target_contrast'] - p[' annulus_contrast']
        contrast = contrast_all[annulus_target_contrast>=0.75]
        this_correct = correct[annulus_target_contrast>=0.75]
        hit_amps = contrast[this_correct==1]
        miss_amps = contrast[this_correct==0]
    all_amps = np.hstack([hit_amps,miss_amps])
    #For psignifit, the data needs to have the form:
    #(stimulus_intensities,n_correct,n_trials)
    stim_intensities = np.unique(all_amps)
    n_correct = [len(np.where(hit_amps==i)[0]) for i in stim_intensities]
    n_trials = [len(np.where(all_amps==i)[0]) for i in stim_intensities]

    constraints = ( 'unconstrained', 'unconstrained', 'unconstrained') 

    #Do the psignifit thing for the psychometric curve:
    Data = zip(stim_intensities,n_correct,n_trials)
    #Both tasks are honest-to-god 2AFC:
    B = BootstrapInference ( data, priors=constraints, nafc=2 )
    B.sample()
    print 'Threshold: %s'%(B.getThres())
    print 'CI: [%s,  %s]'%(B.getCI(1)[0],
                           B.getCI(1)[1])
    print 'Last value in the staircase: %s'%contrast[-1]
           

import sys

from psychopy import gui
from matplotlib.mlab import csv2rec
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.optimize import leastsq

import analysis_utils as ana

if __name__=="__main__":

    bootstrap_n = 1000

    #Weibull params:
    guess = 0.25 #The guessing rate is 0.25 for 4afc
    flake = 0.01
    slope = 3.5
    file_name = str(gui.fileOpenDlg(tryFilePath='./data')[0])
    p, l, data_rec = ana.get_data(file_name) 

    data_rec = csv2rec(file_name)
    annulus_target_contrast = data_rec['annulus_target_contrast']
    block_type = data_rec['block_type']
    correct = data_rec['correct']

    #Which staircase to analyze:
    if p['task'] == ' Fixation ':
        contrast_all = data_rec['fixation_target_contrast']
    elif p['task']== ' Annulus ':
        contrast_all = data_rec['annulus_target_contrast']

    labelit = ['annulus_off','annulus_on']
    #Switch on the two annulus tasks (annulus on vs. annulus off):
    for idx_block, i in enumerate(['B','A']):
        if p['task'] == ' Annulus ':
           contrast = contrast_all[block_type == i]
           this_correct = correct[block_type == i]
           contrast = contrast - p[' annulus_contrast'] *idx_block
        else:
           contrast = contrast_all[block_type == i]
           contrast = contrast - p[' fix_baseline']
           this_correct = correct[block_type == i]
        contrast = contrast[5:]
        this_correct = this_correct[5:]
        file_stem = file_name.split('/')[-1].split('.')[0]
        if not os.path.exists('data/analyzed_data'):
            os.mkdir('data/analyzed_data')

        fig_name = 'data/analyzed_data/%s_%s.png'%(file_stem,labelit[idx_block])
        th,lower,upper = ana.analyze(contrast, this_correct, guess, flake, slope, fig_name)


        print "Task: %s (%s): Threshold estimate: %s, CI: [%s,%s]"%(p['task'],
                                                                    labelit[idx_block],
                                                                    th,
                                                                    lower,
                                                                    upper)


            

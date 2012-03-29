
import sys

from psychopy import gui,core
from matplotlib.mlab import csv2rec
import os
import numpy as np

import analysis_utils as ana

contrast_A = []
correct_A = []
contrast_B = []
correct_B = []

if __name__=="__main__":

    bootstrap_n = 1000

    #Weibull params set in analysis_utils: The guessing rate is 0.25 for 4afc
    guess = 0.25
    flake = 0.01
    slope = 3.5

    file_names = gui.fileOpenDlg(tryFilePath='./data')
    contrast_A = []
    correct_A = []
    contrast_B = []
    correct_B =[]
    for file_idx, file_name in enumerate(file_names):
        if file_idx == 0:
            file_stem =  file_name.split('/')[-1].split('.')[0]
        else:
            file_stem = file_stem + file_name[-8]
        p, l, data_rec = ana.get_data(str(file_name))
        trials_per_condition = float(p[' trials_per_block'])*(float(p[' num_blocks'])/2.0)
        contrast_A.append(np.ones(trials_per_condition,1)
        correct_A.append(np.ones(trials_per_condition,1)
        contrast_B.append(np.ones(trials_per_condition,1)
        correct_B.append(np.ones(trials_per_condition,1)
        data_rec = csv2rec(file_name)
        contrast_this_run = data_rec['annulus_target_contrast']
        correct_this_run = data_rec['correct']
        block_type = data_rec['block_type']

        if not os.path.exists('data/analyzed_data'):
            os.mkdir('data/analyzed_data')
        labelit = ['annulus_on','annulus_off']
        for idx_block,i in enumerate(['A','B']):
            print labelit[idx_block]
            contrast_this_block = contrast_this_run[block_type == i]
            correct_this_block = correct_this_run[block_type == i]
            if i == 'A':
                if p['task'] == ' Annulus ':
                    contrast_this_block = contrast_this_block - p[' annulus_contrast']
                for n in range(trials_per_condition):
                    contrast_A[n+(trials_per_condition*file_idx)] *= contrast_this_block[n]
                    correct_A[n+(trials_per_condition*file_idx)] *= correct_this_block[n]
                #print contrast_this_block, correct_this_block
                block_file_stem = file_stem + '_' + labelit[idx_block]
                fig_name_A = 'data/analyzed_data/%s.png'%(block_file_stem)
        else:
                contrast_this_block = contrast_this_block[p[' trials_per_dummy']:]
                correct_this_block = correct_this_block[p[' trials_per_dummy']:]
                for n in range(trials_per_condition):
                    contrast_B[n+(trials_per_condition*file_idx)] *= contrast_this_block[n]
                    correct_B[n+(trials_per_condition*file_idx)] *= correct_this_block[n]
                block_file_stem = file_stem + '_' + labelit[idx_block]
                fig_name_B = 'data/analyzed_data/%s.png'%(block_file_stem)
            #fig_name = 'data/analyzed_data/%s.png'%(file_stem)

    th,lower,upper = ana.analyze(contrast_A, correct_A, guess, flake, slope, fig_name_A)
    print "Threshold estimate: %s, CI: [%s,%s]"%(th, lower, upper)
    th,lower,upper = ana.analyze(contrast_B, correct_B, guess, flake, slope, fig_name_B)
    print "Threshold estimate: %s, CI: [%s,%s]"%(th, lower, upper)





 

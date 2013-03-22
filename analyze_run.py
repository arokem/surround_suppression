
import sys

from psychopy import gui,core
from matplotlib.mlab import csv2rec
import os
import numpy as np

import analysis_utils as ana

contrast = []
correct = []

if __name__=="__main__":

    bootstrap_n = 1000

    #Weibull params set in analysis_utils: The guessing rate is 0.25 for 4afc
    guess = 0.5
    flake = 0.01
    slope = 3.5

    file_names = gui.fileOpenDlg(tryFilePath='./data')

    for file_idx, file_name in enumerate(file_names):
        print file_idx
        if file_idx == 0:
            file_stem =  file_name.split('/')[-1].split('.')[0]
        else:
            file_stem = file_stem + file_name[-8]
        p, l, data_rec = ana.get_data(str(file_name))
        trials_per_condition = float(p[' trials_per_block'])*(float(p[' num_blocks'])/2.0)
        print trials_per_condition
        contrast = np.ones([len(file_names)*trials_per_condition,1])
        correct = np.ones([len(file_names)*trials_per_condition,1])
        data_rec = csv2rec(file_name)
        contrast_this_run = data_rec['annulus_target_contrast']
        correct_this_run = data_rec['correct']
        block_type = data_rec['block_type']
        print p[' trials_per_dummy']
        for n in range(trials_per_condition):
            if n >= p[' trials_per_dummy']:
                contrast[n+(trials_per_condition*file_idx)] *= contrast_this_run[n]
                correct[n+(trials_per_condition*file_idx)] *= correct_this_run[n]
        if not os.path.exists('data/analyzed_data'):
            os.mkdir('data/analyzed_data')
        labelit = ['annulus_on','annulus_off']
        for idx_block,i in enumerate(['A','B']):
            contrast_this_block = contrast_this_run[block_type == i]
            correct_this_block = correct_this_run[block_type == i]
            if i == 'A':
                if p['task'] == ' Annulus ':
                    contrast_this_block = contrast_this_block - p[' annulus_contrast']
            else:
                print i
                contrast_this_block = contrast_this_block[p[' trials_per_dummy']:]
                correct_this_block = correct_this_block[p[' trials_per_dummy']:]
            block_file_stem = file_stem + '_' + labelit[idx_block]
            fig_name = 'data/analyzed_data/%s.png'%(block_file_stem)
            th,lower,upper = ana.analyze(contrast_this_block, correct_this_block, guess, flake, slope, fig_name)


            print "Threshold estimate: %s, CI: [%s,%s]"%(th, lower, upper)



 

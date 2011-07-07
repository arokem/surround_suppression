import sys

from psychopy import gui
from matplotlib.mlab import csv2rec
import os
import numpy as np

import analysis_utils as ana

if __name__=="__main__":

    bootstrap_n = 1000

    #Weibull params:
    guess = 0.25 #The guessing rate is 0.25 for 4afc
    flake = 0.01
    slope = 3.5
    file_names = gui.fileOpenDlg(tryFilePath='./data')
    for file_name in file_names:
        p, l, data_rec = ana.get_data(str(file_name))

        data_rec = csv2rec(file_name)
        contrast = data_rec['annulus_target_contrast']
        correct = data_rec['correct']

        file_stem = file_name.split('/')[-1].split('.')[0]
        if not os.path.exists('data/analyzed_data'):
            os.mkdir('data/analyzed_data')

        fig_name = 'data/analyzed_data/%s.png'%(file_stem)
        th,lower,upper = ana.analyze(contrast, correct, guess, flake, slope, fig_name)


        print "Threshold estimate: %s, CI: [%s,%s]"%(th, lower, upper)




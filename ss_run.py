"""This actually runs the experiment """ 


import numpy as np
from psychopy import gui



if __name__ == "__main__":
""" The main function"""
    
win = visual.Window([800,600],allowGUI=True)


info = dict(id='',condition=) 
gui = gui.DlgFromDict(dictionary=info,title='Enter run info')

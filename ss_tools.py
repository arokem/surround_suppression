import time
import os

import wx
import numpy as np
from matplotlib.mlab import window_hanning

#Sound-generation function:
def sound_freq_sweep(startFreq, endFreq, duration, samples_per_sec=None):
    """   
    Creates a normalized sound vector (duration seconds long) where the
    frequency sweeps from startFreq to endFreq (on a log2 scale).

    Parameters
    ----------

    startFreq: float, the starting frequency of the sweep in Hz
    
    endFreq: float, the ending frequency of the sweep in Hz

    duration: float, the duration of the sweep in seconds

    samples_per_sec: float, the sampling rate, defaults to 44100 


    """
    if samples_per_sec is None:
        samples_per_sec = 44100

    time = np.arange(0,duration*samples_per_sec)

    if startFreq != endFreq:
        startFreq = np.log2(startFreq)
        endFreq = np.log2(endFreq)
        freq = 2**np.arange(startFreq,endFreq,(endFreq-startFreq)/(len(time)))
        freq = freq[:time.shape[0]]
    else:
        freq = startFreq
    
    snd = np.sin(time*freq*(2*np.pi)/samples_per_sec)

    # window the sound vector with a 50 ms raised cosine
    numAtten = np.round(samples_per_sec*.05);
    # don't window if requested sound is too short
    if len(snd) >= numAtten:
        snd[:numAtten/2] *= window_hanning(np.ones(numAtten))[:numAtten/2]
        snd[-(numAtten/2):] *= window_hanning(np.ones(numAtten))[-(numAtten/2):]

    # normalize
    snd = snd/np.max(np.abs(snd))

    return snd

#User input GUI:
class GetFromGui(wx.Dialog):
    """ Allows user to set input parameters of ss through a simple GUI"""    
    def __init__(self, parent, id, title, combo_choices=['No Choices Given']):
        wx.Dialog.__init__(self, parent, id, title, size=(280, 300))
        # Add text labels
        wx.StaticText(self, -1, 'Subject ID:', pos=(10,20))
        wx.StaticText(self, -1, 'Surround Orientation:', pos=(10,60))
        wx.StaticText(self, -1, 'Annulus Orientation:', pos=(10, 120))
        wx.StaticText(self, -1, 'Task:', pos=(30,200))

        # Add the subj id text box, drop down menu, radio buttons
        self.textbox = wx.TextCtrl(self, -1, pos=(100,18), size=(150, -1))

        #Spin control for the surround orientation:
        self.sc_surround = wx.SpinCtrl(self, -1, '', (140,80))
        self.sc_surround.SetRange(0,180)
        self.sc_surround.SetValue(0)

        #Spin control for the annulus orientation:
        self.sc_annulus = wx.SpinCtrl(self, -1, '', (140,140))
        self.sc_annulus.SetRange(0,180)
        self.sc_annulus.SetValue(0)
                      
        #Radio buttons for the different tasks:
        self.rb_task1 = wx.RadioButton(self, -1, 'Annulus', (95, 200),
                                  style=wx.RB_GROUP)
        self.rb_task2 = wx.RadioButton(self, -1, 'Fixation', (175, 200))
        self.rb_task1.SetValue(1)

        # Add OK/Cancel buttons
        wx.Button(self, 1, 'Done', (60, 240))
        wx.Button(self, 2, 'Quit', (150, 240))
        
        # Bind button press events to class methods for execution
        self.Bind(wx.EVT_BUTTON, self.OnDone, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=2)
        self.Centre()
        self.ShowModal()        

    # If "Done" is pressed, set important values and close the window
    def OnDone(self,event):
        self.success = True
        self.subject = self.textbox.GetValue()
        #If subjet is not set, default to 'test_subject':
        if self.subject == '':
            self.subject == 'test_subject'
        
        if self.rb_task1.GetValue():
            self.TaskType = 'Annulus'
        else:
            self.TaskType = 'Fixation'

        self.surround_ori = self.sc_surround.GetValue()
        self.annulus_ori = self.sc_annulus.GetValue()
        
        self.Close()

    # If "Exit is pressed", toggle failure and close the window
    def OnClose(self, event):
        self.success = False
        self.Close()
    

def start_data_file(subject_id):

    """Start a file object into which you will write the data, while making
    sure not to over-write previously existing files """
    
    #Check the data_file:
    
    list_data_dir = os.listdir('./data')

    i=1
    this_data_file = 'SS_%s_%s_%s.dat'%(subject_id,time.strftime('%m%d%Y'),i)

    while this_data_file in list_data_dir:
        i += 1
        this_data_file='SS_%s_%s_%s.dat'%(subject_id,time.strftime('%m%d%Y'),i)
        
    #Open the file for writing into:
    f = file('./data/%s'%this_data_file,'w')
    #Write some header information
    f.write('## Parameters: ##\n')
    
    return f


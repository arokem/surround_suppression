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
        wx.Dialog.__init__(self, parent, id, title, size=(280, 190))
        # Add text labels
        wx.StaticText(self, -1, 'Subject ID:', pos=(10,20))
        wx.StaticText(self, -1, 'Stimulus:', pos=(10,60))
        wx.StaticText(self, -1, 'Task:', pos=(10, 100))

        # Add the subj id text box, drop down menu, radio buttons
        self.textbox = wx.TextCtrl(self, -1, pos=(100,18), size=(150, -1))
        #Add the drop down menu
        self.combobox = wx.ComboBox(self, -1, pos=(100, 58), size=(150, -1),
            choices=combo_choices, style=wx.CB_READONLY)
        self.combobox.SetSelection(0)
        
        #Radio buttons for the different tasks:
        self.rb1 = wx.RadioButton(self, -1, 'Annulus', (95, 100),
                                  style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(self, -1, 'Fixation', (175, 100))
        self.rb1.SetValue(1)

        # Add OK/Cancel buttons
        wx.Button(self, 1, 'Done', (60, 135))
        wx.Button(self, 2, 'Quit', (150, 135))
        
        # Bind button press events to class methods for execution
        self.Bind(wx.EVT_BUTTON, self.OnDone, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=2)
        self.Centre()
        self.ShowModal()        

    # If "Done" is pressed, set important values and close the window
    def OnDone(self,event):
        self.success = True
        self.subject = self.textbox.GetValue()
        self.stimulus_condition = self.combobox.GetSelection()
        if self.rb1.GetValue():
            self.TaskType = 'Annulus'
        else:
            self.TaskType = 'Fixation'
        self.Close()

    # If "Exit is pressed", toggle failure and close the window
    def OnClose(self, event):
        self.success = False
        self.Close()
    




import wx

class GetFromGui(wx.Dialog):
    """ Allows user to set input parameters of ss through a simple GUI"""    
    def __init__(self, parent, id, title, combo_choices=['No Choices Given']):
        wx.Dialog.__init__(self, parent, id, title, size=(280, 190))
        # Add text labels
        wx.StaticText(self, -1, 'Subject ID:', pos=(10,20))
        wx.StaticText(self, -1, 'Combo Box:', pos=(10,60))
        wx.StaticText(self, -1, 'Task Type:', pos=(10, 100))
        # Add OK/Cancel buttons
        wx.Button(self, 1, 'Done', (60, 135))
        wx.Button(self, 2, 'Exit', (150, 135))
        # Add the subj id text box, drop down menu, radio buttons
        self.textbox = wx.TextCtrl(self, -1, pos=(100,18), size=(150, -1))
        self.combobox = wx.ComboBox(self, -1, pos=(100, 58), size=(150, -1),
            choices=combo_choices, style=wx.CB_READONLY)
        self.combobox.SetSelection(0)
        self.rb1 = wx.RadioButton(self, -1, 'Annulus', (95, 100), style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(self, -1, 'Fixation', (175, 100))
        self.rb1.SetValue(1)
        # Bind button press events to class methods for execution
        self.Bind(wx.EVT_BUTTON, self.OnDone, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=2)
        self.Centre()
        self.ShowModal()        
    # If "Done" is pressed, set important values and close the window
    def OnDone(self,event):
        self.Success = True
        self.Subj = self.textbox.GetValue()
        self.ComboNum = self.combobox.GetSelection()
        self.ComboString = self.combobox.GetStringSelection()
        if self.rb1.GetValue():
            self.TaskType = 'Annulus'
        else:
            self.TaskType = 'Fixation'
        self.Close()
    # If "Exit is pressed", toggle failure and close the window
    def OnClose(self, event):
        self.Success = False
        self.Close()



# Create wx application and instance of user interface
app = wx.App()
user_choice = GetFromGui(None, -1, 'Session Params', ['Choice 1', 'Choice 2'])
# Get params from GUI class if user pressed Done
if user_choice.Success:
    user_params = {
    "Subject" : user_choice.Subj,
    "ComboNum" : user_choice.ComboNum,
    "ComboString" : user_choice.ComboString,
    "TaskType" : user_choice.TaskType}
# Stop execution of the window
user_choice.Destroy()
app.MainLoop()
# Print user params if they exist
try: user_params
except:
    print "Program terminated by user."
else:
    for i in user_params.keys():
        print i, ":", user_params[i]




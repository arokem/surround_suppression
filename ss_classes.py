"""Base classes for the surround suppression experiment

- Stimulus
- Staircase
- Trial

""" 

import numpy as np
from psychopy import core, visual, event
from psychopy.sound import SoundPyglet as Sound


class Params(object):
    """
    The Params class stores all of the parameters needed during
    the execution of ss_run. Runtime variables are set through gui, a priori
    variables are read in from file (default: ss_params.py). All variables
    within Params are private must be read/set through methods.
        
    """
    def __init__(self, p_file='ss_params'):
        #The following params are read in from a file with dict p.
        im = __import__(p_file)
        self.__pedestal_inner = im.p['inner_radius']
        self.__pedestal_outer = im.p['outer_radius']
        self.__pedestal_contrast = im.p['pedestal_contrast']
        self.__surround_size = im.p['surround_size']
        self.__surround_angle = im.p['surround_angle']
        self.__surround_contrast = im.p['surround_contrast']
        self.__ring_width = im.p['ring_width']
        self.__spoke_width = im.p['spoke_width']
        self.__spatial_freq = im.p['spatial_freq']
        self.__spatial_phase = im.p['spatial_phase']
        self.__temporal_freq = im.p['temporal_freq']
        self.__temporal_phase = im.p['temporal_phase']
        self.__stim_duration = im.p['stim_duration']
        self.__response_duration = im.p['response_duration']
        self.__feedb_duration = im.p['feedb_duration']
        #The following params are set post execution within ss_run
        self.__subject_id = None
        self.__results_name = None
        self.__fix_or_ann = None
        
    def __getitem__(self, choice):
        #Returns value of the chosen variable. Use: A = Params['var_name']
        result = {
            'pedestal_inner'    : self.__pedestal_inner,
            'pedestal_outer'    : self.__pedestal_outer,
            'pedestal_contrast' : self.__pedestal_contrast,
            'surround_size'     : self.__surround_size,
            'surround_angle'    : self.__surround_angle,
            'surround_contrast' : self.__surround_contrast,
            'ring_width'        : self.__ring_width,
            'spoke_width'       : self.__spoke_width,
            'spatial_freq'      : self.__spatial_freq,
            'spatial_phase'     : self.__spatial_phase,
            'temporal_freq'     : self.__temporal_freq,
            'temporal_phase'    : self.__temporal_phase,
            'stim_duration'     : self.__stim_duration,
            'response_duration' : self.__reponse_duration,
            'feedb_duration'    : self.__feedb_duration
        }[choice]        
        return result
    
    def __setitem__(self, choice, new_value):
        #Sets the chosen runtime variable. Use: Params['var_name'] = A
        if choice == 'subject_id':
            self.__subject_id = new_value
        elif choice == 'results_name':
            self.__results_name = new_value
        elif choice == 'fix_or_ann':
            self.__fix_or_ann = new_value
        else:
            print "Can't assign there"
        


class Event(object):

    """This is the base clase for the events, which sets the template for all
    the events objects """
    def __init__(self,win,**kwargs):
        """
        This always initializes with the window object and with a params
        object
        
        
        """
        #The event has to be attached to some psychopy window object:
        self.win = win 

        #The duration attribute is also necessary: 
        if 'duration' in kwargs.keys():
            self.duration = kwargs['duration']
        else:
            self.duration = 0
            
        #Set the rest of the attributes, if they are provided:
        for k in kwargs:
            self.__setattr__(k,kwargs[k])

    def finalize(self,**kwargs):
        """
        This is a function to finalize the event, before making it happen

        """
        #In the simplest case, just set additional attributes according to the
        #input: 
        for k in kwargs:
            self.__setattr__(k,kwargs[k])
        
    def __call__(self,**kwargs):
        """
        Make the event go for the alloted duration

        This method overloads the __call__ method allowing directly calling 
        the object with the inputs for the event occurence

        """
        
        #Allow to set the duration at this point as well (which would
        #over-ride any previous setting):
        if 'duration' in kwargs.keys():
            self.duration = kwargs['duration']
        

        #In the simplest case, just clear the screen completely at each refresh:
        clock = core.Clock()
        t=0
        while t<self.duration: #Keep going for the duration
            t=clock.getTime()
            #For each of the object attributes, go and check whether it has a
            #'draw' method. If it does, call that method before flipping the
            #window, so that if stimuli objects from psychopy were provided,
            #those will be shown for the duration: 
            for k in self.__dict__:
                try:
                    self.__dict__[k].draw()
                except: #Do nothing in case of an exception:
                    pass
            self.win.flip()

        #Return the entire object at the end, so that we can inspect it:
        return self
    
class Staircase(object):
    """
    This is an object for holding, updating and potentially analyzing
    A psychophysical staircase

    """ 
    def __init__(self,start,step,n_up=3,n_down=1,harder=-1,ub=1,lb=0):
        """
        Initialization function for the staircase class

        Parameters
        ----------
        start: The starting value of the staircase
        step: The size of the step used when updating the staircase
        n_up,n_down: The kind of staircase to be used, defaults to a 3-up,
                     1-down staircase 

        harder: {-1,1} The direction which would make the task harder. Defaults
        to -1, which is true for the contrast decrement detection task.

        """
        self.value = start
        self.n_up = n_up
        self.step = step
        self.n = 0 #This is what will be compared to n_up for udpating.
        self.harder = np.sign(harder) #Make sure that this is only -1 or 1.
        self.record = [start]
        
    def update(self,correct):
        """

        This function updates the staircase value, according to the state of
        the staircase, the n/n_up values and whether or not the subject got it
        right. This staircase is then propagated on to the next trial.

        Parameters
        ----------
        correct: {True|False} 

        """

        if correct:
            if self.n>=self.n_up-1:
                self.value += self.harder * self.step #'harder' sets the sign
                                                      #of the change to make it
                                                      #harder
                self.n = 0
            else:
                self.n +=1
                
        else:
            self.n = 0
            self.value -= self.harder * self.step #Change in the
                                        #opposite direction than above to make
                                        #it easier!

        #Add to the records the updated value: 
        self.record.append(self.value)
    
      
class Stimulus(Event):

    """The surround suppression stimulus, including everything """

    def __init__(self,win,params,surround_contrast=None,surround_ori=None,
                 annulus_contrast=None, annulus_ori=None, fixation_ori=None,
                 fixation_color=None,
                 tex_res = 256):
        """

        Initialize the object, by setting all the various subobjects

        Parameters
        ----------

        win: a psychopy window object

        params: an object with parameters for setting the size and . Note that
        the units of size here need to be the units that were used to
        initialize the window object (should be degrees).

        surround_contrast, surround_ori, annulus_contrast, annulus_ori: These
        variables can be used in order to over-ride the values of these
        variables in the params object. They cannot be set online, after the
        object has been initialized, except by calling the setters of the
        psychopy objects.

        fixation_ori: sometimes we might want to rotate the fixation square to
        some other orientation. This allows this. Defaults to None => upright
        square. 

        fixation_color: If we want to change the color of the fixation from
        white (the default) to some other color (rgb argument). 

        
        tex_res: the resolution (in pixels) at which the OpenGL texture is
        rendered (?).
        """

        #Carry the window object around with you:
        self.win = win
        #The resolution for the textures:
        self.tex_res = tex_res
        #The temporal frequency of the flicker:
        self.temporal_freq = params.temporal_freq

        #Set the params for the different components of the stimulus. The
        #default is to follow what is given by the params:
        if surround_contrast is None:
            surround_contrast = params.surround_contrast
        if surround_ori is None:
            surround_ori = params.surround_ori
        if annulus_contrast is None:
            annulus_contrast = params.annulus_contrast
        if annulus_ori is None:
            annulus_ori = params.annulus_ori
        
        #Set both parts of the surround
        self.outer_surround = visual.PatchStim(self.win,tex="sin",mask="circle",
                                           texRes=tex_res,
                                           color=surround_contrast,
                                           size=(params.surround_outer-
                                                 params.ring_width/2,
                                                 params.surround_outer-
                                                 params.ring_width/2),
                                           sf=params.spatial_freq,
                                           ori = surround_ori)

        self.inner_surround = visual.PatchStim(self.win,tex="sin",mask="circle",
                                               texRes=tex_res,
                                               color=surround_contrast,
                                               size=(params.annulus_inner-
                                                     params.ring_width/2,
                                                     params.annulus_inner-
                                                     params.ring_width/2),
                                               sf=params.spatial_freq,
                                               ori = surround_ori)

        #Set the annulus:
        self.annulus = visual.PatchStim(self.win,tex="sin",mask="circle",
                                        texRes=tex_res,
                                        color=annulus_contrast,
                                        size=(params.annulus_outer-
                                              params.ring_width/2,
                                              params.annulus_outer-
                                              params.ring_width/2),
                                        sf=params.spatial_freq,
                                        ori = annulus_ori)

        #Set the rings abutting the annulus on both sides:
        ring_width = params.ring_width
        spoke_width = params.spoke_width
        #This is the bit between the annulus and the outer surround: 
        self.ring1 = visual.PatchStim(self.win, tex=None, mask='circle',
                                      color=-1, #Always black
                                      size=[params.annulus_outer+ring_width/2,
                                            params.annulus_outer+ring_width/2],
                                      interpolate=True)

        #This is the bit between the annulus and the inner surround: 
        self.ring2 = visual.PatchStim(self.win, tex=None, mask='circle',
                                      color=-1, #Always black
                                      size=[params.annulus_inner+ring_width/2,
                                            params.annulus_inner+ring_width/2],
                                      interpolate=True)

        #This is the central area, between the inner surround and the fixation: 
        self.center_area = visual.PatchStim(self.win, tex=None, mask='circle',
                                            color=0, #Always gray
                                            size=params.surround_inner,
                                            interpolate=True)

        self.spokes = []
        for i in np.arange(num_spokes/2):
            self.spokes.append(visual.ShapeStim(self.win,
                                fillColor = -1,
                                lineColor = -1,
                                vertices = ((-spoke_width/2,annulus_outer/2),
                                            (spoke_width/2,-annulus_outer/2),
                                            (-spoke_width/2,-annulus_outer/2),
                                            (spoke_width/2,annulus_outer/2)),
                                ori=i*45))

        # Fixation (made out of two concentric squares):
        # Set the fixation parameters from the input or the defaults:
        if fixation_color is None:
            fixation_color = 1
        if fixation_ori is None:
            fixation_ori = 0

        self.fixation = visual.PatchStim(self.win, tex=None,
                                         color=fixation_color,
                                         size=fixation_size,
                                         interpolate=True,
                                         ori=fixation_ori)

        self.fixation_center = visual.PatchStim(self.win, tex=None,
                                                color=-1,
                                                size=fixation_size/4,
                                                interpolate=True,
                                                ori=fixation_ori)

        def finalize(self,params,target_co=None,target_loc=None,
                     target_ori=None,fixation_co=None):

            """

            Finalize the stimulus, by setting the target

            Parameters
            ----------

            params: a parameter object with all the pre-defined params

            target_co: the contrast of the target in this trial (set by the
            staircase). Set to None if no target is to be set in this stimulus
            object 

            target_loc: the location of the target (integer between 0 and 7) in
            this trial. defaults to None => random location

            target_ori: The orientation of the target (typically set to the
            same orientation as the annulus). Defaults to None => the
            orientation given in the params object

            fixation_co: This allows setting of the fixation contrast (the
            difference between white and black), so that it can serve as a
            target.

            """
            if target_co is None: 
                #Set the target to None per default:
                self.target = None
            #If a target is to be shown, proceed on to set it:
            else: 
                #Throw errors if the contrast values don't make sense:
                if target_co > params.pedestal_contrast:
                    raise ValueError ("Target contrast cannot be larger than the pedestal contrast: %s" %params.pedestal_contrast)

                if target_co < params.min_contrast:
                    raise ValueError("Target contrast cannot be smaller than the minimal contrast: %s"%params.min_contrast) 

                if target_loc is None:
                    #Choose a random one between 0 and 7 (with equal
                    #probabilities):
                    target_loc = int(np.random.rand(1) * 8)
                if target_ori is None:
                    #Get it from the params:
                    target_ori = params.target_ori
                    
                #In order to apply a different contrast to the target wedge,
                #generate a mask, which will cover everything except for the
                #target wedge:
                grid_array = np.linspace(-1*self.annulus.size[0],
                                         self.annulus.size[0],
                                         annulus.texRes)

                x,y=np.meshgrid(grid_array,grid_array)
                r = np.sqrt(x**2 + y**2)
                theta = np.arctan2(x,y) + np.pi
                target_mask = np.ones((self.annulus.texRes,self.annulus.texRes))

                target_mask[np.where(r>params.annulus_outer-
                                     params.ring_width/2)] = -1

                target_mask[np.where(r<params.annulus_inner-
                                     params.ring_width/2)] = -1

                #Since the whole PatchStim is rotated according to annulus_ori,
                #we need to adjust for that, so that the target locations
                #remain invariant across different orientations (hence
                #subtraction of annulus_ori):
                target_mask[np.where(theta<target_loc*np.deg2rad(45)-
                                     np.deg2rad(annulus_ori))] = -1
                target_mask[np.where(theta>(target_loc+1)*np.deg2rad(45)-
                                     np.deg2rad(target_ori))] = -1

                #Now show the target contrast in the wedge, using that mask:
                self.target = visual.PatchStim(self.win,tex="sin",
                                               mask=target_mask,
                                               texRes=self.tex_res,
                                               color=target_co, 
                                               size=(params.annulus_outer-
                                                     params.ring_width/2,
                                                     params.annulus_outer-
                                                     params.ring_width/2),
                                               sf=params.spatial_freq,
                                               ori=target_ori)

                #If you want to set the fixation target with a contrast value:
                if fixation_co is not None:
                    #Set the fixation target somehow
                    self.fixation.setContrast(fixation_co)
                    self.fixation_center.setContrast(fixation_co)    
                    
        def __call__(self,params,duration=0):
            #Choose a random phase (btwn -pi and pi) to start the presentation
            #with:
            ph_rand = (np.random.rand(1) * 2*np.pi) - np.pi
            #Start a clock 
            clock = core.Clock()
            while t<duration: #Keep going for the duration
                t=clock.getTime()

                self.annulus.setContrast(np.sin(ph_rand +
                                                t*self.temporal_freq*np.pi*2))
                self.inner_surround.setContrast(np.sin(ph_rand +
                                                t*self.temporal_freq*np.pi*2))
                self.outer_surround.setContrast(np.sin(ph_rand +
                                                t*self.temporal_freq*np.pi*2))
                
                if self.target is not None: 
                    self.target.setContrast(np.sin(ph_rand +
                                            t*self.temporal_freq*np.pi*2))

                #Draw them (order matters!)
                if self.outer_surround is not None:
                    self.outer_surround.draw()
                self.ring1.draw()
                self.annulus.draw()
                if self.target is not None:
                    self.target_wedge.draw()
                for spoke in self.spokes:
                    spoke.draw()
                self.ring2.draw()
                self.inner_surround.draw()
                self.center_area.draw()
                self.fixation.draw()
                self.fixation_center.draw()
                
                win.flip() #update the screen
                
            #Return the object, so that we can inspect it:
            return self
        
class WaitForButton(Event):
    """
    A class which waits with whatever is on the screen until a button is
    pressed. This can wait for either a particular button (such as the ttl
    pulse from the scanner) or any old button (when initiating the experiment
    by the subject).

    """
    def __init__(self,win):

        
    
class Text(Event):

    """

    A class for showing text on the screen. The text persists after
    presenting it, unless otherwise indicated. Text is always shown at the
    center of the screen, white on gray. 

    """

    def __init__ (self,win,text=''):
        """ """

    #No need for a 'finalize' method in this case.
    
    def __call__(self):
        """ """ 
    
class Response(Event):

    """
    Getting responses from subjects and
    
    """
def sound_freq_sweep(startFreq, endFreq, duration, samplesPerSec=None):
 """   
 Creates a normalized sound vector (duration seconds long) where the
 frequency sweeps from startFreq to endFreq (on a log2 scale).

 samplesPerSec is optional- the system-wide default sample rate of 8192
 will be used if not specified.

 example: 
 t = fsweep(100, 500, .2);

"""
if samples_per_sec is None:
    samplesPerSec = 8192;

time = np.arange(0,duration*samplesPerSec)


if startFreq != endFreq:
    startFreq = np.log2(startFreq)
    endFreq = np.log2(endFreq)
    freq = 2.^[startFreq:(endFreq-startFreq)/(length(time)-1):endFreq];
else:
    freq = startFreq

snd = sin(time.*freq*(pi*2)/samplesPerSec);

% window the sound vector with a 50 ms raised cosine
numAtten = round(samplesPerSec*.05);
% don't window if requested sound is too short
if length(snd) >= numAtten
    snd = cosWindow(snd, numAtten);
end

% normalize
snd = snd/max(abs(snd));


function x = cosWindow(x, numAtten)
% x = cosWindow(x, numAtten) windows the vector X by a raised cosine.
% numAtten specifies the number of values at the beginning and end of
% X to attenuate with the window.
%
% September 13, 1998 Bob Dougherty

if nargin~=2
    error('Usage: out = cosWindow(x, numAtten)')
end

if numAtten<1 return; end    % do nothing

[m,n] = size(x);
if min(n,m) > 1    
    error('x must be a vector')
end
l = max(m,n);
if l < numAtten    
    error('length of x must be > or = numAtten')
end

wind = 0.5*cos([pi:pi/(numAtten-1):2*pi])+.5;
if n==1
    wind = wind';
    x(1:numAtten) = x(1:numAtten).*wind;
    x(l-numAtten+1:l) = x(l-numAtten+1:l).*fliplr(wind')';
else
    x(1:numAtten) = x(1:numAtten).*wind;
    x(l-numAtten+1:l) = x(l-numAtten+1:l).*fliplr(wind);
end

    
class Feedback(Event):

    def __init__(self):
        """This provides auditory feedback (and visual?) about performance """ 

        self.incorrect_sound =
        self.correct_sound =
        self.no_respones_sound = 
